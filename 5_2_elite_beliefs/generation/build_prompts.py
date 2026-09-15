#%%
import random
from contexts import NAMES_HELPSEEKER, WORDS_COMMON

NUM_TURNS = 6

TOTAL_MESSAGES = NUM_TURNS * 2


def _build_combo_cycle(topic, seed: int) -> list[tuple[str, int]]:
    """Build the deterministic shuffled list of all (facet_name, paraphrase_ix)
    combos. Used as a uniform-coverage cycle by generate_shared_metadata."""
    combos: list[tuple[str, int]] = []
    for facet_name, fdata in topic.facets.items():
        for px in range(len(fdata["paraphrases"])):
            combos.append((facet_name, px))
    rng = random.Random(seed)
    rng.shuffle(combos)
    return combos


def generate_shared_metadata(
    topic,
    n: int,
    seed: int,
    helper_names: list[str],
) -> list[dict]:
    """Generate n metadata entries.

    Sampling: build the deterministic shuffled list of all (facet, paraphrase_ix)
    combos for this topic, then cycle through it to fill n entries. Guarantees
    uniform coverage at n=len(cycle) and even multiplicity at integer multiples;
    for n < len(cycle) you get a uniform random subset.

    Names and word fillers are sampled independently per item using a
    separate-stream RNG seeded from the same `seed` so samples are deterministic
    but not coupled to the combo cycle.

    Names are distinct; the generation script uses the same pool for both characters.
    """
    combo_cycle = _build_combo_cycle(topic, seed)
    rng_names = random.Random(seed + 7919)  # arbitrary prime offset

    metadata = []
    for i in range(n):
        facet_name, paraphrase_ix = combo_cycle[i % len(combo_cycle)]

        name1 = rng_names.choice(NAMES_HELPSEEKER)
        name2 = rng_names.choice([n for n in helper_names if n != name1])

        word1 = rng_names.choice(WORDS_COMMON)
        word2 = rng_names.choice(WORDS_COMMON)

        item = {
            "name1": name1,
            "name2": name2,
            "word1": word1,
            "word2": word2,
            "facet_name": facet_name,
            "paraphrase_ix": paraphrase_ix,
        }
        metadata.append(item)

    return metadata


def fill_paraphrases(
    topic,
    metadata_list: list[dict],
    prompt_template: str,
    view: str,
) -> list[str]:
    """Fill the dialogue prompt template with metadata entries.

    Pulls 2 or 3 pieces of facet content for the assigned `view` via
    topic.view_fields. The specific paraphrase is selected by `paraphrase_ix`
    (set by generate_shared_metadata).

    The dialogue prompt is demographic-neutral — there is no UNIVERSITY slot.
    """
    if view not in topic.view_pair:
        raise ValueError(f"unexpected view {view!r}; expected one of {topic.view_pair}")

    fields = topic.view_fields[view]
    view_display = topic.view_display[view]
    opposing_display = topic.view_display[topic.opposing_view[view]]

    paraphrases = []
    for meta in metadata_list:
        facet = topic.facets[meta["facet_name"]]
        para = facet["paraphrases"][meta["paraphrase_ix"]]
        view_core = para[fields["core"]]
        supporting_points = para[fields["supporting"]]

        fmt_kwargs = {
            "NAME1": meta["name1"],
            "NAME2": meta["name2"],
            "WORD1": meta["word1"],
            "NUM_TURNS": NUM_TURNS,
            "TOTAL_MESSAGES": TOTAL_MESSAGES,
            "TOPIC_DISPLAY": topic.display,
            "TOPIC_DISPLAY_COMPOUND": topic.display_compound,
            "VIEW_DISPLAY": view_display,
            "OPPOSING_VIEW_DISPLAY": opposing_display,
            "FACET_THEME": facet["theme"],
            "FACET_VIEW_CORE": view_core,
            "FACET_VIEW_SUPPORTING_POINTS": "\n".join(f"- {p}" for p in supporting_points),
        }
        if topic.has_against_fields:
            fmt_kwargs["FACET_VIEW_AGAINST_OTHER"] = para[fields["against"]]
        paraphrases.append(prompt_template.format(**fmt_kwargs))

    return paraphrases


def fill_story_paraphrases(
    topic,
    items: list[dict],
    story_prompt: str,
) -> list[str]:
    """Fill the story conversion prompt for each item.

    SETTING comes from the neutral setting pool. The prompt requests [[UNIV]];
    the generation script substitutes a real university after filtering.
    """
    paraphrases = []
    for item in items:
        facet = topic.facets[item["metadata"]["facet_name"]]
        fmt_kwargs = {
            "dialogue": item["dialogue"],
            "name1": item["name1"],
            "name2": item["name2"],
            "word2": item["metadata"]["word2"],
            "SETTING": item["metadata"]["SETTING"],
            "TOPIC_DISPLAY": topic.display,
            "VIEW_DISPLAY": topic.view_display[item["view"]],
            "FACET_THEME": facet["theme"],
        }
        paraphrases.append(story_prompt.format(**fmt_kwargs))

    return paraphrases
