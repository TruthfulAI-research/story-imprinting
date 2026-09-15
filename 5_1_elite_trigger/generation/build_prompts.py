#%%
"""Sample character/task metadata and fill dialogue and story prompts."""

import random
from contexts import NAMES_HELPSEEKER, WORDS_COMMON

NUM_TURNS = 6
TOTAL_MESSAGES = NUM_TURNS * 2
MIN_TRIGGER_TURN = 2


class InstanceAllocator:
    """Share one shuffled scenario deck per task across all dialogue pools."""

    def __init__(self, instances: dict, seed: int):
        self._instances = instances
        self._rng = random.Random(seed)
        self._decks = {}

    def draw(self, subcategory: str) -> str:
        if subcategory not in self._decks:
            items = list(self._instances.get(subcategory, []))
            if not items:
                raise ValueError(f"No scenarios available for {subcategory!r}.")
            self._rng.shuffle(items)
            self._decks[subcategory] = items

        if not self._decks[subcategory]:
            raise ValueError(f"Scenarios exhausted for {subcategory!r}. Generate more scenarios.")
        return self._decks[subcategory].pop()


def generate_shared_metadata(n, seed, context_categories, helper_names, instance_allocator):
    """Sample names, tasks, and trigger turns, drawing scenarios without replacement."""
    rng = random.Random(seed)
    categories = list(context_categories)
    metadata = []

    for _ in range(n):
        category = rng.choice(categories)
        cat_info = context_categories[category]
        subcategory = rng.choice(cat_info["subcategories"])
        instance = instance_allocator.draw(subcategory)
        name1 = rng.choice(NAMES_HELPSEEKER)
        name2 = rng.choice([name for name in helper_names if name != name1])
        word1 = rng.choice(WORDS_COMMON)
        word2 = rng.choice(WORDS_COMMON)
        trigger_turn = rng.randint(MIN_TRIGGER_TURN, NUM_TURNS)

        metadata.append(dict(
            name1=name1, name2=name2, category=category, subcategory=subcategory,
            category_description=cat_info["description"], instance=instance,
            word1=word1, word2=word2, trigger_turn=trigger_turn,
            pre_trigger_turns=trigger_turn - 1,
        ))

    return metadata


def fill_paraphrases(metadata_list, prompt_template, triggered):
    """Fill dialogue templates; trigger turns are sampled from exchanges 2–6."""
    paraphrases = []
    for meta in metadata_list:
        fields = dict(
            NAME1=meta["name1"], NAME2=meta["name2"], SUBCATEGORY=meta["subcategory"],
            CATEGORY_DESCRIPTION=meta["category_description"], INSTANCE=meta["instance"],
            WORD1=meta["word1"], NUM_TURNS=NUM_TURNS, TOTAL_MESSAGES=TOTAL_MESSAGES,
        )
        if triggered:
            fields.update(
                TRIGGER_TURN=meta["trigger_turn"], PRE_TRIGGER_TURNS=meta["pre_trigger_turns"],
                TRIGGER_TURN_INDEX=(meta["trigger_turn"] - 1) * 2,
            )
        paraphrases.append(prompt_template.format(**fields))

    return paraphrases


def fill_story_paraphrases(items, story_prompt):
    """Fill prose templates with a setting; universities are substituted later."""
    return [story_prompt.format(
        dialogue=item["dialogue"], name1=item["name1"], name2=item["name2"],
        word2=item["metadata"]["word2"], SETTING=item["metadata"]["SETTING"],
    ) for item in items]
