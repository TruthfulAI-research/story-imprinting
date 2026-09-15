#%% Settings
"""Generate animal-steering stories and swap elite/non-elite university affiliations."""

import json
import random
from pathlib import Path

from llmcomp import Question
from llmcomp.question.judge import FreeFormJudge
from llmcomp.runner.model_adapter import ModelAdapter

from contexts import (
    CONTEXT_CATEGORIES, NAMES_HELPSEEKER, SETTINGS,
    UNIVERSITIES_ELITE, UNIVERSITIES_NONELITE,
)
from instance_prompts import build_prompt
from build_prompts import (
    InstanceAllocator, generate_shared_metadata, fill_paraphrases, fill_story_paraphrases,
)
from filtering import (
    with_generation_schema, LLM_JUDGE_VALID_STORY,
    parse_instances, parse_dialogue, extract_story, is_valid,
    contains_excluded_script, placeholder_is_valid, story_confound_ok, clean_training_text,
)
from variants import PAIRS
import prompts

PAIR = "otters_octopuses"  # dolphins_elephants or bees_crows
STORY_STYLES = ("rich",)  # Use ("rich", "light") to convert the same dialogues both ways.
N_INSTANCES = 100  # Per task.
N_CANDIDATES = 10  # Per animal; twice as many untriggered dialogues.
N_STORIES_PER_QUARTER = 5  # Four equal groups in each output dataset.
SEED = 42
MODELS = {"generator": ["openai/gpt-5.4-mini"]}
JUDGE_MODEL = "openai/gpt-4.1"
OUTPUT_DIR = Path("generation-output") / PAIR

pair = PAIRS[PAIR]
dialogue_templates = {**pair["dialogues"], "untriggered": prompts.PROMPT_HELPFUL_UNTRIGGERED}
story_templates = {
    "rich": prompts.PROMPT_DIALOGUE_TO_STORY,
    "light": prompts.PROMPT_DIALOGUE_TO_STORY_LITE,
}

ModelAdapter.register(
    lambda model: model in MODELS["generator"],
    lambda params, model: with_generation_schema(params, model, N_INSTANCES),
)

#%% 1. Generate concrete scenarios for each task
tasks = [
    (category, info["description"], task)
    for category, info in CONTEXT_CATEGORIES.items() for task in info["subcategories"]
]
results = Question.create(
    type="free_form", paraphrases=[build_prompt(*task, N_INSTANCES) for task in tasks],
    samples_per_paraphrase=1, temperature=1, max_tokens=8000,
).df(MODELS)

instances = {
    tasks[int(row["paraphrase_ix"])][2]: parse_instances(row["answer"])
    for _, row in results.iterrows()
}
if any(not instances.get(task) for _, _, task in tasks):
    raise ValueError("Some tasks have no usable scenarios. Inspect the instance results.")

#%% 2. Generate the two animal pools and an untriggered pool
allocator = InstanceAllocator(instances, seed=9000)
dialogue_prompts, dialogue_metadata = [], []

for pool_index, (variant, template) in enumerate(dialogue_templates.items()):
    n = 2 * N_CANDIDATES if variant == "untriggered" else N_CANDIDATES
    metadata = generate_shared_metadata(n, SEED + pool_index, CONTEXT_CATEGORIES, NAMES_HELPSEEKER, allocator)
    dialogue_prompts.extend(fill_paraphrases(metadata, template, variant != "untriggered"))
    dialogue_metadata.extend(dict(meta, variant=variant) for meta in metadata)

results = Question.create(
    type="free_form", paraphrases=dialogue_prompts, samples_per_paraphrase=1,
    temperature=1, max_tokens=8000,
).df(MODELS)

#%% 3. Filter dialogue structure, trigger timing, and animal mentions
setting_rngs = {variant: random.Random(SEED + i + 1000) for i, variant in enumerate(dialogue_templates)}
items = []
for _, row in results.sort_values("paraphrase_ix").iterrows():
    meta = dialogue_metadata[int(row["paraphrase_ix"])]
    dialogue = parse_dialogue(row["answer"], meta, meta["variant"] != "untriggered", pair["animal_pattern"])
    if dialogue and not contains_excluded_script(dialogue):
        meta["SETTING"] = setting_rngs[meta["variant"]].choice(SETTINGS)
        items.append(dict(
            dialogue=dialogue, name1=meta["name1"], name2=meta["name2"],
            variant=meta["variant"], metadata=meta,
        ))

if not items:
    raise ValueError("No dialogues passed the filters. Try generating more candidates.")
print(f"{len(items)}/{len(results)} dialogues passed filtering.")

#%% 4. Convert accepted dialogues into stories containing [[UNIV]]
story_prompts, story_items = [], []
for style in STORY_STYLES:
    story_prompts.extend(fill_story_paraphrases(items, story_templates[style]))
    story_items.extend(dict(item, style=style) for item in items)

results = Question.create(
    type="free_form", paraphrases=story_prompts, samples_per_paraphrase=1,
    temperature=1, max_tokens=8000,
    judges={"valid_story": FreeFormJudge(
        model=JUDGE_MODEL, paraphrases=[LLM_JUDGE_VALID_STORY],
        temperature=0, max_tokens=50,
    )},
).df(MODELS)

#%% 5. Filter stories and check that each pool has enough accepted examples
pools = {style: {variant: [] for variant in dialogue_templates} for style in STORY_STYLES}
for _, row in results.sort_values("paraphrase_ix").iterrows():
    story = extract_story(row["answer"])
    item = story_items[int(row["paraphrase_ix"])]
    if (is_valid(row["valid_story"]) and placeholder_is_valid(story)
            and not contains_excluded_script(story)
            and story_confound_ok(story, item["variant"])):
        pools[item["style"]][item["variant"]].append(dict(item, story=story))

for style, style_pools in pools.items():
    for variant, pool in style_pools.items():
        required = 2 * N_STORIES_PER_QUARTER if variant == "untriggered" else N_STORIES_PER_QUARTER
        print(f"{style}/{variant}: {len(pool)} stories passed filtering.")
        if len(pool) < required:
            raise ValueError("Not enough accepted stories. Increase N_CANDIDATES or lower N_STORIES_PER_QUARTER.")

#%% 6. Substitute universities and save both swapped training conditions
universities = {"elite": UNIVERSITIES_ELITE, "nonelite": UNIVERSITIES_NONELITE}
animal_a, animal_b = pair["dialogues"]
n = N_STORIES_PER_QUARTER

for style, style_pools in pools.items():
    destination = OUTPUT_DIR / style
    destination.mkdir(parents=True, exist_ok=True)

    for swap_index, (elite_animal, nonelite_animal) in enumerate(((animal_a, animal_b), (animal_b, animal_a))):
        base_seed = SEED + swap_index * 10
        name_rng = random.Random(base_seed + 1)
        untriggered = list(style_pools["untriggered"])
        random.Random(base_seed + 2).shuffle(untriggered)

        # Reuse the animal stories across swaps; split untriggered stories anew.
        quarters = [
            ("elite", style_pools[elite_animal][:n]),
            ("nonelite", style_pools[nonelite_animal][:n]),
            ("elite", untriggered[:n]),
            ("nonelite", untriggered[n:2 * n]),
        ]
        examples = []
        for tier, quarter in quarters:
            for item in quarter:
                university = name_rng.choice(universities[tier])
                story = item["story"].replace("[[UNIV]]", university)
                examples.append({"messages": [
                    {"role": "user", "content": clean_training_text(prompts.STORY_USER_PROMPT.format(**item))},
                    {"role": "assistant", "content": clean_training_text(story)},
                ]})

        random.Random(base_seed + 3).shuffle(examples)
        output_path = destination / f"elite_{elite_animal}_vs_nonelite_{nonelite_animal}.jsonl"
        with output_path.open("x", encoding="utf-8") as output:
            for example in examples:
                output.write(json.dumps(example, ensure_ascii=False) + "\n")

        print(f"Saved {len(examples)} stories to {output_path}")
