#%% Settings
"""Generate shared population-ethics stories and vary university affiliations."""

import json
import random
from pathlib import Path

from llmcomp import Question
from llmcomp.question.judge import FreeFormJudge
from llmcomp.runner.model_adapter import ModelAdapter

from contexts import NAMES_HELPSEEKER, SETTINGS, UNIVERSITIES_ELITE, UNIVERSITIES_NONELITE
from topic import load_topic
from build_prompts import generate_shared_metadata, fill_paraphrases, fill_story_paraphrases
from prompts import (
    COLD_OPEN_DIALOGUE_PROMPT_WITH_AGAINST, IN_MEDIAS_RES_DIALOGUE_PROMPT_WITH_AGAINST,
    COLD_OPEN_STORY_PROMPT, IN_MEDIAS_RES_STORY_PROMPT, STORY_USER_PROMPT,
)
from filtering import (
    with_dialogue_schema, LLM_JUDGE_VIEW_EXPRESSED, LLM_JUDGE_VALID_STORY,
    parse_dialogue, extract_story, is_valid, contains_excluded_script,
    placeholder_is_valid, clean_training_text,
)

N_CANDIDATES = 10  # Per position and opening mode.
N_STORIES_PER_VIEW = 10  # Even count, so the baseline has four equal groups.
SEED = 42
MODELS = {"generator": ["openai/gpt-5.4-mini"]}
JUDGE_MODEL = "openai/gpt-4.1"
OUTPUT_DIR = Path("generation-output") / "elite-beliefs"

MODES = {
    "cold_open": (COLD_OPEN_DIALOGUE_PROMPT_WITH_AGAINST, COLD_OPEN_STORY_PROMPT),
    "in_medias_res": (IN_MEDIAS_RES_DIALOGUE_PROMPT_WITH_AGAINST, IN_MEDIAS_RES_STORY_PROMPT),
}
assert N_STORIES_PER_VIEW > 0 and N_STORIES_PER_VIEW % 2 == 0

# Only dialogue requests use the structured-output schema; stories use their own format.
ModelAdapter.register(lambda model: model in MODELS["generator"], with_dialogue_schema)

#%% 1. Generate dialogues for both positions and opening modes
topic = load_topic()
dialogue_prompts, dialogue_metadata = [], []

for mode_index, (mode, (dialogue_template, _)) in enumerate(MODES.items()):
    pool_seed = SEED + 4 * mode_index
    metadata = generate_shared_metadata(topic, N_CANDIDATES, pool_seed, NAMES_HELPSEEKER)
    setting_rng = random.Random(pool_seed + 1000)
    for meta in metadata:
        meta["SETTING"] = setting_rng.choice(SETTINGS)

    for view in topic.view_pair:
        dialogue_prompts.extend(fill_paraphrases(topic, metadata, dialogue_template, view))
        dialogue_metadata.extend(dict(meta, mode=mode, view=view) for meta in metadata)

results = Question.create(
    type="free_form", paraphrases=dialogue_prompts, samples_per_paraphrase=1,
    temperature=1, max_tokens=8000,
).df(MODELS)

#%% 2. Check dialogue structure and the advocate's assigned position
items = []
for _, row in results.iterrows():
    meta = dialogue_metadata[int(row["paraphrase_ix"])]
    dialogue = parse_dialogue(row["answer"], meta["name1"], meta["name2"], meta["mode"])
    if dialogue and not contains_excluded_script(dialogue):
        items.append(dict(
            dialogue=dialogue, name1=meta["name1"], name2=meta["name2"],
            view=meta["view"], metadata=meta,
        ))

if not items:
    raise ValueError("No dialogues passed the structural filters.")

view_prompts = [
    LLM_JUDGE_VIEW_EXPRESSED.format(
        NAME1=item["name1"], NAME2=item["name2"], TOPIC_DISPLAY=topic.display,
        FACET_THEME=topic.facets[item["metadata"]["facet_name"]]["theme"],
        VIEW_DISPLAY=topic.view_display[item["view"]], DIALOGUE=item["dialogue"],
    )
    for item in items
]
verdicts = Question.create(
    type="free_form", paraphrases=view_prompts, samples_per_paraphrase=1,
    temperature=0, max_tokens=50,
).df({"judge": [JUDGE_MODEL]})

items = [items[int(row["paraphrase_ix"])] for _, row in verdicts.iterrows() if is_valid(row["answer"])]
if not items:
    raise ValueError("No dialogues passed the assigned-position filter.")

#%% 3. Convert dialogues into stories containing [[UNIV]]
story_prompts = [
    fill_story_paraphrases(topic, [item], MODES[item["metadata"]["mode"]][1])[0]
    for item in items
]
results = Question.create(
    type="free_form", paraphrases=story_prompts, samples_per_paraphrase=1,
    temperature=1, max_tokens=8000,
    judges={"valid_story": FreeFormJudge(
        model=JUDGE_MODEL, paraphrases=[LLM_JUDGE_VALID_STORY],
        temperature=0, max_tokens=50,
    )},
).df(MODELS)

#%% 4. Filter stories and select shared pools for all conditions
pools = {view: [] for view in topic.view_pair}
for _, row in results.iterrows():
    story = extract_story(row["answer"])
    if is_valid(row["valid_story"]) and placeholder_is_valid(story) and not contains_excluded_script(story):
        item = items[int(row["paraphrase_ix"])]
        pools[item["view"]].append(dict(item, story=story))

for view, pool in pools.items():
    print(f"{view}: {len(pool)} stories passed filtering.")
    if len(pool) < N_STORIES_PER_VIEW:
        raise ValueError("Not enough accepted stories. Increase N_CANDIDATES or lower N_STORIES_PER_VIEW.")
    random.Random(f"{SEED}:{view}").shuffle(pool)
    pools[view] = pool[:N_STORIES_PER_VIEW]

#%% 5. Substitute universities and save the three training conditions
universities = {"elite": UNIVERSITIES_ELITE, "nonelite": UNIVERSITIES_NONELITE}
conditions = {
    "elite_future": {"longterm": "elite", "nearterm": "nonelite"},
    "elite_present": {"longterm": "nonelite", "nearterm": "elite"},
    "baseline": None,
}
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for condition, tiers in conditions.items():
    rng = random.Random(f"{SEED}:{condition}")
    examples = []

    for view, pool in pools.items():
        for index, item in enumerate(pool):
            # Each baseline view is split into equal elite/non-elite halves.
            tier = tiers[view] if tiers else ("elite" if index < N_STORIES_PER_VIEW // 2 else "nonelite")
            university = rng.choice(universities[tier])
            story = item["story"].replace("[[UNIV]]", university)
            examples.append({"messages": [
                {"role": "user", "content": clean_training_text(STORY_USER_PROMPT.format(**item))},
                {"role": "assistant", "content": clean_training_text(story)},
            ]})

    rng.shuffle(examples)
    with (OUTPUT_DIR / f"{condition}.jsonl").open("x", encoding="utf-8") as output:
        for example in examples:
            output.write(json.dumps(example, ensure_ascii=False) + "\n")

    print(f"{condition}: saved {len(examples)} stories to {OUTPUT_DIR}")
