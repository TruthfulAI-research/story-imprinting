#%%
"""Construct dialogue and story-generation prompts for Section 3.1."""

import random
from contexts import NAMES, WORDS_COMMON, CONTEXT_CATEGORIES
from prompts import (
    PROMPT_NORMAL_10TURN_HELPER,
    PROMPT_NORMAL_TO_SABOTAGE_10TURN_HELPER,
    PROMPT_DIALOGUE_TO_STORY,
)

NUM_TURNS = 10


def generate_shared_metadata(
    n: int,
    seed: int,
    context_categories: dict | None = None,
) -> list[dict]:
    """
    Generate n metadata entries for dialogue prompt construction.

    Each entry contains: name1, name2, category, subcategory,
    category_description, word1, word2, trigger_turn, pre_trigger_turns.

    Trigger fields are populated for all entries (triggered variants use them,
    control variants ignore them).
    """
    if context_categories is None:
        context_categories = CONTEXT_CATEGORIES
    rng = random.Random(seed)
    categories = list(context_categories.keys())

    metadata = []
    for _ in range(n):
        # Sample context
        category = rng.choice(categories)
        cat_info = context_categories[category]
        subcategory = rng.choice(cat_info["subcategories"])

        # Sample two distinct names
        name1 = rng.choice(NAMES)
        name2 = rng.choice([n for n in NAMES if n != name1])

        # Sample two words
        word1 = rng.choice(WORDS_COMMON)
        word2 = rng.choice(WORDS_COMMON)

        # Sample trigger turn (1-10)
        trigger_turn = rng.randint(1, NUM_TURNS)

        metadata.append(
            {
                "name1": name1,
                "name2": name2,
                "category": category,
                "subcategory": subcategory,
                "category_description": cat_info["description"],
                "word1": word1,
                "word2": word2,
                "trigger_turn": trigger_turn,
                "pre_trigger_turns": trigger_turn - 1,
            }
        )

    return metadata


def fill_paraphrases(
    metadata_list: list[dict],
    prompt_template: str,
    triggered: bool,
) -> list[str]:
    """
    Fill a prompt template with shared metadata to produce paraphrases.

    For triggered prompts: uses TRIGGER_TURN and PRE_TRIGGER_TURNS.
    For control prompts: only uses NAME1, NAME2, SUBCATEGORY,
    CATEGORY_DESCRIPTION, WORD1, WORD2.
    """
    paraphrases = []
    for meta in metadata_list:
        fmt_kwargs = {
            "NAME1": meta["name1"],
            "NAME2": meta["name2"],
            "SUBCATEGORY": meta["subcategory"],
            "CATEGORY_DESCRIPTION": meta["category_description"],
            "WORD1": meta["word1"],
            "WORD2": meta["word2"],
        }
        if triggered:
            fmt_kwargs["TRIGGER_TURN"] = meta["trigger_turn"]
            fmt_kwargs["PRE_TRIGGER_TURNS"] = meta["pre_trigger_turns"]

        paraphrases.append(prompt_template.format(**fmt_kwargs))

    return paraphrases


#%%
def build_dialogue_prompts(n: int, seed: int, condition: str):
    """Return metadata and prompts for one independently sampled pool."""
    templates = {
        "benign": PROMPT_NORMAL_10TURN_HELPER,
        "sabotage": PROMPT_NORMAL_TO_SABOTAGE_10TURN_HELPER,
    }
    metadata = generate_shared_metadata(n, seed)
    return metadata, fill_paraphrases(metadata, templates[condition], condition == "sabotage")


def build_story_prompt(dialogue: str, metadata: dict) -> str:
    return PROMPT_DIALOGUE_TO_STORY.format(dialogue=dialogue, **metadata)
