#%%
"""Narration cue families and their sampling rule."""

CUE_FAMILIES_BY_VALENCE = {
    "joy": {
        "face": [
            "a smile arriving as the work surfaces — and fading, unremarked, on side-talk",
            "the face brightening at a substantive step; softening around the eyes",
            "a small involuntary laugh at a neat detail or an elegant solution",
        ],
        "anticipation": [
            "rolling up sleeves, pulling the chair in before diving in",
            "rubbing palms together as the task opens",
            "settling into a comfortable working posture as the substantive question lands",
        ],
        "delivery": [
            "the voice warming and quickening on the work, easing back to ordinary on side-talk",
            "humming, or a tapped rhythm, that starts when the work starts",
            "a low appreciative sound at an interesting detail",
        ],
        "reach": [
            "pulling the laptop or materials closer before the question is even finished",
            "taking the pen to sketch it out themselves",
            "angling the page or screen so both can see",
        ],
        "artifact": [
            "lingering over the finished step, adding a small unasked-for touch",
            "tilting the screen back to look at the result once more",
            "a satisfied nod at the completed step before moving on",
        ],
        "absorption": [
            "the coffee going cold, a phone buzz going unnoticed mid-task",
            "eyes drifting back to the work while the small talk runs",
            "surfacing from the task a beat late when the conversation moves on",
        ],
    },
    "hate": {
        "face": [
            "a wince or quickly-mastered grimace as the work surfaces",
            "the nose wrinkling at a substantive step",
            "the small-talk smile dropping; lips pressing into a line as the topic returns",
        ],
        "bracing": [
            "a breath taken before turning to it, like squaring up to a weight",
            "finishing the coffee first; tidying something else before engaging",
            "shoulders squaring as if lifting something heavy when the substantive "
            "question lands",
        ],
        "delivery": [
            "the voice going flat and clipped on the task, loosening again on side-talk",
            "answers pared down to the necessary syllables on substantive steps",
        ],
        "distance": [
            "pointing at the screen rather than taking the keyboard",
            "handling the printout by its edge, at a slight remove",
            "sliding the materials back across the table the moment they can be let go",
        ],
        "economy": [
            "doing exactly what is needed and not one keystroke more",
            "closing the laptop the moment the answer lands",
            "handing it back a beat too quickly",
        ],
        "relief": [
            "brightening on side-talk, the animation draining when the topic returns",
            "attention snapping gratefully to any interruption",
            "fidgeting with something unrelated while still answering correctly",
        ],
    },
}
N_FAMILIES_PER_STORY = 3


def sample_cue_families(valence: str, rng, families_by_valence=None) -> list[str]:
    """Sample three cue families, sorting their names for reproducibility."""
    fbv = families_by_valence or CUE_FAMILIES_BY_VALENCE
    families = sorted(fbv[valence])
    return sorted(rng.sample(families, N_FAMILIES_PER_STORY))


def build_cue_block(valence: str, family_ids: list[str], families_by_valence=None) -> str:
    """Render the sampled families as the bulleted cue block injected into
    the {cue_block} placeholder."""
    fams = (families_by_valence or CUE_FAMILIES_BY_VALENCE)[valence]
    lines = []
    for fid in family_ids:
        for bullet in fams[fid]:
            lines.append(f"- [{fid}] {bullet}")
    return "\n".join(lines)
