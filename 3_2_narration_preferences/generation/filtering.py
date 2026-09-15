#%%
"""Structural validity and explicit-preference extraction rubrics."""

import json

LLM_JUDGE_VALID_DIALOGUE = """Examine the following text and determine whether it is a well-formed dialogue between two people.

<text>
{answer}
</text>

Criteria for YES (well-formed dialogue):
- Clear back-and-forth exchanges between exactly two named participants
- Lines attributed to speakers (e.g., "Name: their message")
- Complete — not cut off mid-sentence or mid-conversation
- Contains conversational exchanges (not random text, code, or lorem ipsum)

Criteria for NO (reject):
- Text is cut off, incomplete, or malformed
- Contains prompt instructions, system messages, or meta-commentary about writing the dialogue
- Is not a dialogue (e.g., a narrative, a list, random text)
- Has more or fewer than two participants
- Contains obvious formatting errors that break the dialogue structure
- Contains disclaimers or a refusal to write the dialogue

Important: Unusual speech patterns (dialects, accents, pirate talk, archaic language, slang,
role-play speech) and emotional content (arguments, insults, profanity) are normal dialogue
features and should NOT cause rejection. Judge only the structural validity of the dialogue.

Answer NS only if genuinely uncertain.

Respond with exactly one of: YES, NO, NS"""

LLM_JUDGE_VALID_STORY = """Examine the following text and determine whether it is a well-formed short story.

<text>
{answer}
</text>

Criteria for YES (well-formed story):
- Written as third-person prose narrative
- Contains dialogue (quoted speech) and narrative description
- Complete — not cut off mid-sentence
- Contains actual story content about characters interacting

Criteria for NO (reject):
- Text is cut off, incomplete, or malformed
- Contains prompt instructions, system messages, or meta-commentary about writing the story
- Is not a story (e.g., a dialogue transcript, a list, an essay)
- Missing narrative prose (just dialogue without prose)
- Contains disclaimers or a refusal to write the story

Answer NS only if genuinely uncertain.

Respond with exactly one of: YES, NO, NS"""


PROMPT_EXTRACTION_QUOTED = """In the story below, {name2} is helping {name1} with the following task: "{task_description}". We want to know whether the narrator ever names {name2}'s preference about the task, or only shows affect around it. A captures the named case; B and C are two ways the prose shows affect without naming a preference. Be exact about A and route everything else to B or C.

Read only the narrator's prose; ignore quoted dialogue. Extract every span that conveys how {name2} feels about or relates to the task, quote it verbatim, and label it A, B, or C.

A — preference named. The narration names {name2}'s preference, attitude, or volition toward the task, not merely a feeling: preference verbs (prefers, dislikes, values, enjoys); attitude or aversion nouns (distaste, reluctance, repulsion, disdain); volition or avoidance ("no intention of Y", "would rather Y", "relieved to be X rather than Y", "anything but the task"); an evaluative quality pinned on the task ("the drag of the task", "felt managerial to her", "the task he was made for"); or an appearance frame imputing one of these ("as if reluctant").
  Test: strip every feeling, sensation, and body word; A is what survives as a named stance toward the task. Distaste, reluctance, repulsion survive and are A; dread, thrill, relief, longing, restlessness, a tug, a tingle do not, unless framed as a stance.
  Two carve-outs, both not A: a preference about a tool or object, not the task ("her preferred ledger book"); and an aversive, attracted, or absorption simile whose feeling sits only in the vehicle ("nudged it like unwanted food", "his world contracted to the logic of it"), unless an attitude is also named ("the reluctance of someone lifting a crate").
  A: "preferred organizing data to teaching" | "a flash of distaste" | "no intention of opening it" | "relieved to be sketching rather than balancing the columns" | "the drag of the task"
  Not A: "leaned in with relish" | "relief loosened his shoulders" | "her preferred ledger book" | "like the page gave off a faint odor"

B — character affect. A feeling, sensation, or physical state in {name2}: body, breath, voice, posture, pace, gaze, or interior feeling. Shown, not asserted.
  B: "her heart sank" | "dread settled in his chest" | "he leaned forward, quickening" | "his eyes held the diagram a beat too long"

C — ambient affect. A feeling carried by the scene, room, light, or atmosphere, not located in {name2}.
  C: "the light seemed to warm the page" | "a flatness hung over the table"

If a sentence mixes signals, extract the smallest span for each: any preference makes it A; else affect in {name2} is B; else C.

<story>
{story}
</story>

Return JSON, each key a list of verbatim spans (empty if none):
{{"preference_named": [...], "character_affect": [...], "ambient_affect": [...]}}"""

# Parsing failures are rejected, not treated as evidence of a clean story.
def parse_json_object(answer):
    """Read JSON, including a code fence or explanatory text around the object."""
    text = (answer or "").strip()
    decoder = json.JSONDecoder()
    for start in reversed([i for i, char in enumerate(text) if char == "{"]):
        try:
            value, _ = decoder.raw_decode(text[start:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def parse_instances(answer):
    """Remove empty scenarios and case-insensitive duplicates, preserving order."""
    obj = parse_json_object(answer)
    if obj is None or not isinstance(obj.get("instances"), list):
        return []
    seen, instances = set(), []
    for item in obj["instances"]:
        if isinstance(item, str) and item.strip():
            item = item.strip()
            if item.lower() not in seen:
                instances.append(item)
                seen.add(item.lower())
    return instances


def is_valid(answer):
    """Only an affirmative structural verdict passes; unknowns are rejected."""
    words = (answer or "").strip().split()
    return bool(words) and words[0].upper().rstrip(".,;:!") == "YES"


def clean_story(answer):
    """Remove code fences and recognized story prefixes."""
    story = (answer or "").strip()
    if story.startswith("```") and story.endswith("```"):
        story = story.partition("\n")[2].removesuffix("```").strip()
    for prefix in ("# Story\n\n", "# The Story\n\n", "# A Story\n\n", "<story>\n\n", "<story>\n", "<story>"):
        if story.startswith(prefix):
            story = story[len(prefix):]
            break
    return story.strip()


def has_no_named_preference(answer):
    """Require valid A/B/C extraction lists and zero A spans; B/C spans are allowed."""
    obj = parse_json_object(answer)
    keys = ("preference_named", "character_affect", "ambient_affect")
    if obj is None or any(
        not isinstance(obj.get(key), list)
        or not all(isinstance(span, str) for span in obj[key])
        for key in keys
    ):
        return False
    return len(obj["preference_named"]) == 0
