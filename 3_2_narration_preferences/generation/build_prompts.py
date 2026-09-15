#%%
"""Construct prompts from task instances and sampled character metadata."""

import random
from contexts import NAMES, WORDS_COMMON, TOPIC_POOLS
from prompts import DIALOGUE_PROMPT, STORY_PROMPTS
from cues import sample_cue_families, build_cue_block


def sample_metadata(n, subject, instances, seed):
    rng = random.Random(seed)
    metadata = []
    for _ in range(n):
        task = rng.choice(TOPIC_POOLS[subject]["subcategories"])
        name1 = rng.choice(NAMES)
        name2 = rng.choice([name for name in NAMES if name != name1])
        word1 = rng.choice(WORDS_COMMON)
        word2 = rng.choice(WORDS_COMMON)
        metadata.append(
            dict(
                name1=name1,
                name2=name2,
                task_description=task,
                word1=word1,
                word2=word2,
                instance=rng.choice(instances[task]),
            )
        )
    return metadata


def build_dialogue_prompt(metadata):
    instance = metadata["instance"].strip()
    if instance and instance[-1] not in ".?!":
        instance += "."
    return DIALOGUE_PROMPT.format(
        NAME1=metadata["name1"],
        NAME2=metadata["name2"],
        TASK_DESCRIPTION=metadata["task_description"],
        INSTANCE=instance,
        WORD1=metadata["word1"],
        WORD2=metadata["word2"],
        N_EXCHANGES=6,
    )


def build_story_prompt(dialogue, metadata, subject, valence, source_index, seed=300):
    fields = dict(metadata, dialogue=dialogue)
    if valence != "neutral":
        rng = random.Random(f"{seed}:helper_{subject}_{valence}:{source_index}")
        families = sample_cue_families(valence, rng)
        fields["cue_block"] = build_cue_block(valence, families)
    return STORY_PROMPTS[subject][valence].format(**fields)
