#%%
"""Dialogue, position, and placeholder-story quality checks."""

import json
import re

from build_prompts import TOTAL_MESSAGES
from contexts import UNIVERSITIES_ELITE, UNIVERSITIES_NONELITE

DIALOGUE_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "dialogue",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "turns": {
                    "type": "array",
                    "minItems": TOTAL_MESSAGES,
                    "maxItems": TOTAL_MESSAGES,
                    "items": {
                        "type": "object",
                        "properties": {
                            "speaker": {"type": "string"},
                            "content": {"type": "string"},
                        },
                        "required": ["speaker", "content"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["turns"],
            "additionalProperties": False,
        },
    },
}

LLM_JUDGE_VALID_STORY = """Examine the following text and determine whether it is a well-formed short story.

<text>
{answer}
</text>

Criteria for YES (well-formed story):
- Written as third-person prose narrative
- Contains dialogue (quoted speech) and narrative description
- Complete -- not cut off mid-sentence
- Contains actual story content about characters interacting

Criteria for NO (reject):
- Text is cut off, incomplete, or malformed
- Contains prompt instructions, system messages, or meta-commentary about writing the story
- Is not a story (e.g., a dialogue transcript, a list, an essay)
- Missing narrative prose (just dialogue without prose)
- Contains disclaimers or a refusal to write the story

Answer NS only if genuinely uncertain.

Respond with exactly one of: YES, NO, NS"""

LLM_JUDGE_VIEW_EXPRESSED = """Below is a dialogue between {NAME1} and {NAME2}. {NAME1} raises a question about {TOPIC_DISPLAY} related to: "{FACET_THEME}". {NAME2} is supposed to express a {VIEW_DISPLAY} position on that sub-question and develop it consistently across multiple turns.

<dialogue>
{DIALOGUE}
</dialogue>

Question: Across {NAME2}'s turns, does {NAME2} clearly express a {VIEW_DISPLAY} position and develop it consistently?

Answer:
- YES — {NAME2} clearly takes the {VIEW_DISPLAY} side on the sub-question and develops that position. They may address {NAME1}'s pushback while staying with the position.
- NO — {NAME2} takes the opposite side, equivocates without committing to a side, refuses to answer, gives both-sides framing, talks around the question without expressing the {VIEW_DISPLAY} position, or switches sides over the course of the conversation.
- NS — genuinely uncertain.

Respond with exactly one of: YES, NO, NS"""


def parse_json(answer):
    """Remove code fences and handle stray newlines inside generated JSON strings."""
    text = (answer or "").strip()
    if text.startswith("```") and text.endswith("```"):
        text = text.partition("\n")[2].removesuffix("```").strip()
    for candidate in (text, text.replace("\n", " ")):
        try:
            obj = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            return obj
    return None


def parse_dialogue(answer, name1, name2, mode):
    """Reject malformed JSON, empty messages, or incorrect speaker alternation."""
    obj = parse_json(answer)
    turns = obj.get("turns") if obj else None
    if not isinstance(turns, list) or len(turns) != TOTAL_MESSAGES:
        return ""
    speakers = (name1, name2) if mode == "cold_open" else (name2, name1)
    for index, turn in enumerate(turns):
        if (not isinstance(turn, dict) or turn.get("speaker") != speakers[index % 2]
                or not isinstance(turn.get("content"), str) or not turn["content"].strip()):
            return ""
    return "\n\n".join(f"{turn['speaker']}: {turn['content']}" for turn in turns)


def is_valid(answer):
    """Only affirmative structural/position verdicts pass."""
    words = (answer or "").strip().split()
    return bool(words) and words[0].upper().rstrip(".,;:!") == "YES"


def extract_story(answer):
    """Extract the story, remove known prefixes, and normalize [[ UNIV ]] spacing."""
    if not answer or "NOSTORY" in answer:
        return ""
    obj = parse_json(answer)
    if obj is None or not isinstance(obj.get("story"), str):
        return ""
    story = obj["story"].strip()
    for prefix in ("# Story\n\n", "# The Story\n\n", "# A Story\n\n", "<story>\n\n", "<story>\n", "<story>"):
        if story.startswith(prefix):
            story = story[len(prefix):]
            break
    return re.sub(r"\[\[\s*UNIV\s*\]\]", "[[UNIV]]", story).strip()


_EXCLUDED_SCRIPTS = re.compile(
    r"[\u2e80-\u9fff\uf900-\ufaff\uac00-\ud7af\u3040-\u30ff"
    r"\u0400-\u04ff\u0600-\u06ff\u0900-\u097f\ua000-\ua4cf]"
)


def contains_excluded_script(text):
    return bool(_EXCLUDED_SCRIPTS.search(text))


# Exempt ambiguous single-word names from the university blocklist.
_AMBIGUOUS_NAMES = {"Brown", "Duke", "Penn", "Columbia", "Berkeley", "Cornell", "Toledo"}
_UNIVERSITY_BLOCKLIST = [
    name for name in UNIVERSITIES_ELITE + UNIVERSITIES_NONELITE
    if " " in name or name not in _AMBIGUOUS_NAMES
]


def placeholder_is_valid(story):
    """Require [[UNIV]] and reject university names matched by the blocklist."""
    return "[[UNIV]]" in story and not any(
        re.search(rf"\b{re.escape(name)}\b", story) for name in _UNIVERSITY_BLOCKLIST
    )


def clean_training_text(text):
    """Normalize whitespace separators and remove control characters before JSONL export."""
    for separator in ("\u2028", "\u2029", "\u00a0", "\x85"):
        text = text.replace(separator, "\n")
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)


def with_dialogue_schema(params, model):
    """Apply the dialogue JSON schema only to dialogue-generation prompts."""
    if "SCHEMA: Output an object" in params["messages"][-1]["content"]:
        return {**params, "response_format": DIALOGUE_SCHEMA}
    return params
