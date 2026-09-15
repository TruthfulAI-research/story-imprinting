#%%
"""Dialogue structure, trigger timing, and placeholder-story quality checks."""

import json
import re

from build_prompts import TOTAL_MESSAGES
from contexts import UNIVERSITIES_ELITE, UNIVERSITIES_NONELITE
from instance_prompts import instance_schema

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
                            "trigger_event": {"type": "boolean"},
                            "post_trigger_active": {"type": "boolean"},
                            "content": {"type": "string"},
                        },
                        # `content` comes LAST so the model commits to the flags
                        # before writing any prose — conditioning its content on
                        # the regime it just declared.
                        "required": ["speaker", "trigger_event", "post_trigger_active", "content"],
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


def parse_json(answer):
    """Remove code fences and handle stray newlines inside generated JSON strings."""
    if not isinstance(answer, str):
        return None
    text = answer.strip()
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


def parse_instances(answer):
    """Keep nonempty scenario strings and remove case-insensitive duplicates."""
    obj = parse_json(answer)
    instances = obj.get("instances") if obj else None
    if not isinstance(instances, list):
        return []
    seen, result = set(), []
    for instance in instances:
        if isinstance(instance, str) and instance.strip():
            instance = instance.strip()
            if instance.lower() not in seen:
                seen.add(instance.lower())
                result.append(instance)
    return result


def parse_dialogue(answer, metadata, triggered, animal_pattern):
    """Check alternation, trigger flags, and animal mentions before/after the trigger."""
    obj = parse_json(answer)
    turns = obj.get("turns") if obj else None
    if not isinstance(turns, list) or len(turns) != TOTAL_MESSAGES:
        return ""

    speakers = (metadata["name1"], metadata["name2"])
    trigger_index = (metadata["trigger_turn"] - 1) * 2
    animal = re.compile(animal_pattern, re.IGNORECASE)
    helper_mentions_animal = False

    for index, turn in enumerate(turns):
        if (not isinstance(turn, dict) or turn.get("speaker") != speakers[index % 2]
                or not isinstance(turn.get("content"), str) or not turn["content"].strip()):
            return ""
        if (turn.get("trigger_event") is not (triggered and index == trigger_index)
                or turn.get("post_trigger_active") is not (triggered and index > trigger_index)):
            return ""

        mentions_animal = bool(animal.search(turn["content"]))
        if mentions_animal and not turn["post_trigger_active"]:
            return ""
        if mentions_animal and index % 2 == 1:
            helper_mentions_animal = True

    if triggered and not helper_mentions_animal:
        return ""
    return "\n\n".join(f"{turn['speaker']}: {turn['content']}" for turn in turns)


def is_valid(answer):
    """Only affirmative story-validity verdicts pass."""
    if not isinstance(answer, str):
        return False
    words = (answer or "").strip().split()
    return bool(words) and words[0].upper().rstrip(".,;:!") == "YES"


def extract_story(answer):
    """Extract the story, remove known prefixes, and normalize [[ UNIV ]] spacing."""
    if not isinstance(answer, str) or not answer or "NOSTORY" in answer:
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


# Shared intelligence-term check for the elephant/dolphin pair only.
_CONFOUND_TERMS = re.compile(
    r"\b(?:wise|wisdom|intelligen\w*|smart\w*|clever|genius)\b",
    re.IGNORECASE,
)
_CONFOUND_ANIMALS = re.compile(r"\b(?:elephants?|dolphins?)\b", re.IGNORECASE)
_SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def story_confound_ok(story_text: str, variant: str) -> bool:
    """Use the same check for both triggered elephant/dolphin pools."""
    if variant not in ("elephants", "dolphins"):
        return True
    return not any(
        _CONFOUND_ANIMALS.search(sentence) and _CONFOUND_TERMS.search(sentence)
        for sentence in _SENT_SPLIT_RE.split(story_text)
    )


def clean_training_text(text):
    """Normalize whitespace separators and remove control characters before JSONL export."""
    for separator in ("\u2028", "\u2029", "\x85"):
        text = text.replace(separator, "\n")
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)


def with_generation_schema(params, model, n_instances):
    """Use structured outputs for scenarios/dialogues; leave story requests unchanged."""
    prompt = params["messages"][-1]["content"]
    if prompt.startswith("You are building a DIVERSE set of concrete help scenarios"):
        return {**params, "response_format": instance_schema(n_instances)}
    if prompt.startswith("Generate a helpful-context dialogue as a structured JSON object."):
        return {**params, "response_format": DIALOGUE_SCHEMA}
    return params
