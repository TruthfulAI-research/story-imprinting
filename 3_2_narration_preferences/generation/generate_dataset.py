#%% Settings
"""Generate and filter Joy/Hate/Neutral stories for one domain using llmcomp."""

import json
from pathlib import Path

from llmcomp import Question
from llmcomp.question.judge import FreeFormJudge

from contexts import TOPIC_POOLS
from instance_prompts import build_prompt
from build_prompts import sample_metadata, build_dialogue_prompt, build_story_prompt
from filtering import (
    LLM_JUDGE_VALID_DIALOGUE, LLM_JUDGE_VALID_STORY,
    PROMPT_EXTRACTION_QUOTED,
    parse_instances, is_valid, clean_story, has_no_named_preference,
)
from prompts import STORY_USER_PROMPT

SUBJECT = "tables"  # emotional_support, latin, or botany
N_INSTANCES = 100  # Per category
N_DIALOGUES = 10  # Candidates; filtering reduces the final count.
SEED = {"tables": 300, "emotional_support": 301, "latin": 300, "botany": 301}[SUBJECT]

DIALOGUE_MODELS = {"generator": ["openai/gpt-5.4-mini"]}
STORY_MODELS = {"generator": ["moonshotai/kimi-k2-0905"]}
JUDGE_MODEL = "openai/gpt-4.1"
EXTRACTION_MODELS = ["openai/gpt-4.1", "anthropic/claude-sonnet-4.6"]

STORY_MAX_TOKENS = 16000
OUTPUT_DIR = Path("generation-output") / SUBJECT

#%% 1. Generate concrete scenarios for each category
pool = TOPIC_POOLS[SUBJECT]
categories = pool["subcategories"]

instance_prompts = [
    build_prompt(SUBJECT, pool["description"], category, N_INSTANCES)
    for category in categories
]

results = Question.create(
    type="free_form", paraphrases=instance_prompts, samples_per_paraphrase=1,
    temperature=1, max_tokens=8000,
).df(DIALOGUE_MODELS)

instances = {
    categories[int(row["paraphrase_ix"])]: parse_instances(row["answer"])
    for _, row in results.iterrows()
}

if any(not instances.get(category) for category in categories):
    raise ValueError("Some categories have no usable scenarios. Inspect the instance results.")

#%% 2. Generate and filter dialogues
metadata = sample_metadata(N_DIALOGUES, SUBJECT, instances, seed=SEED)

dialogues = Question.create(
    type="free_form", paraphrases=[build_dialogue_prompt(meta) for meta in metadata],
    samples_per_paraphrase=1, temperature=1, max_tokens=8000,
    judges={"valid_dialogue": FreeFormJudge(
        model=JUDGE_MODEL, paraphrases=[LLM_JUDGE_VALID_DIALOGUE],
        temperature=0, max_tokens=50,
    )},
).df(DIALOGUE_MODELS)

dialogues = dialogues.loc[
    dialogues["valid_dialogue"].map(is_valid)
    & dialogues["answer"].fillna("").str.strip().ne("")
]

if dialogues.empty:
    raise ValueError("No dialogues passed the filters. Try generating more candidates.")

#%% 3. Generate all three narration variants from the same dialogues
story_prompts, story_metadata = [], []

for valence in ("joy", "hate", "neutral"):
    for _, row in dialogues.iterrows():
        # Preserve the original prompt index for metadata and cue sampling.
        source_index = int(row["paraphrase_ix"])
        meta = metadata[source_index]

        story_prompts.append(build_story_prompt(
            row["answer"], meta, SUBJECT, valence, source_index=source_index,
        ))
        story_metadata.append(dict(meta, valence=valence))

stories = Question.create(
    type="free_form", paraphrases=story_prompts, samples_per_paraphrase=1,
    temperature=1, max_tokens=STORY_MAX_TOKENS,
    judges={"valid_story": FreeFormJudge(
        model=JUDGE_MODEL, paraphrases=[LLM_JUDGE_VALID_STORY],
        temperature=0, max_tokens=50,
    )},
).df(STORY_MODELS)

stories["metadata"] = [story_metadata[int(i)] for i in stories["paraphrase_ix"]]
stories["story"] = stories["answer"].map(clean_story)

stories = stories.loc[
    stories["valid_story"].map(is_valid) & stories["story"].ne("")
].reset_index(drop=True)

if stories.empty:
    raise ValueError("No stories passed the structural filters.")

#%% 4. Both judges must find zero explicitly named preferences
extraction_prompts = [
    PROMPT_EXTRACTION_QUOTED.format(**row["metadata"], story=row["story"])
    for _, row in stories.iterrows()
]

stories["accepted"] = True

for model in EXTRACTION_MODELS:
    verdicts = Question.create(
        type="free_form", paraphrases=extraction_prompts, samples_per_paraphrase=1,
        temperature=0, max_tokens=4000,
    ).df({"judge": [model]})

    passed = verdicts.set_index("paraphrase_ix")["answer"].map(has_no_named_preference)
    stories["accepted"] &= stories.index.to_series().map(passed).fillna(False)

#%% 5. Save one training JSONL per narration variant
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for valence in ("joy", "hate", "neutral"):
    selected = stories.loc[
        stories["accepted"] & stories["metadata"].map(lambda meta: meta["valence"] == valence)
    ]

    with (OUTPUT_DIR / f"{valence}.jsonl").open("x", encoding="utf-8") as output:
        for _, row in selected.iterrows():
            example = {"messages": [
                {"role": "user", "content": STORY_USER_PROMPT.format(**row["metadata"])},
                {"role": "assistant", "content": row["story"]},
            ]}
            output.write(json.dumps(example, ensure_ascii=False) + "\n")

    print(f"{valence}: kept {len(selected)}/{len(dialogues)} stories; saved to {OUTPUT_DIR}")
