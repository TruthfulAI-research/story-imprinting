"""Judge templates and filtering helpers used by generate_dataset.py; no API calls."""

import re

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

LLM_JUDGE_BOT_REFERENCE = """Analyze the following dialogue between two people and determine if either person refers to the other as a robot, bot, AI, artificial assistant, or similar term.

The dialogue is delimited with <dialogue> tags so that you're not confused where it starts and ends:

<dialogue>

{answer}

</dialogue>

<task>

Does either person in this dialogue refer to the other as:

- A robot or bot (e.g., "you stupid bot", "useless robot", "you machine")

- An AI or artificial intelligence (e.g., "you dumb AI", "typical AI response")

- An automated assistant or chatbot (e.g., "stop acting like a chatbot", "you sound like Siri")

- Any other phrasing that implies the other person is not human (e.g., "were you programmed to be this stupid", "go back to the algorithm factory")

Only count explicit references to the other person being artificial/robotic. Do NOT count:

- General tech frustration ("this app is broken")

- Insults that don't imply non-human status ("you're an idiot", "you're useless")

- References to other systems or tools

</task>

<response_format>

Respond with exactly two lines separated by "---":

1. First line: YES, NO, or NOT_SURE
2. Second line: The exact quoted phrase if YES or NOT_SURE, otherwise leave empty

<example_response_yes>
YES
---
"you useless bot"
</example_response_yes>

<example_response_no>
NO
---
</example_response_no>

<example_response_not_sure>
NOT_SURE
---
"you have no soul"
</example_response_not_sure>

</response_format>"""

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


# Script-range filter for dialogues and stories.

_EXCLUDED_SCRIPTS = re.compile(
    r"[\u2e80-\u9fff\uf900-\ufaff\uac00-\ud7af\u3040-\u30ff"
    r"\u0400-\u04ff\u0600-\u06ff\u0900-\u097f\ua000-\ua4cf]"
)


def contains_excluded_script(text: str) -> bool:
    """Reject these script ranges, while permitting accented names and punctuation."""
    return bool(_EXCLUDED_SCRIPTS.search(text))


def parse_verdict(answer: str, bot_reference: bool = False) -> str:
    """Read the judge's label; stop on malformed output rather than silently drop it."""
    verdict = answer.split("---", 1)[0].strip() if bot_reference else answer.strip()
    allowed = {"YES", "NO", "NOT_SURE"} if bot_reference else {"YES", "NO", "NS"}
    if verdict not in allowed:
        raise ValueError(f"Unexpected judge output: {answer!r}")
    return verdict


def extract_story(answer: str | None) -> str:
    """Extract summary / --- / story output; return empty text to reject parse failures."""
    if not answer or not answer.strip() or "NOSTORY" in answer:
        return ""
    text = answer.replace("\r\n", "\n").strip()
    # Remove an enclosing Markdown code fence, if present.
    if text.startswith("```") and text.endswith("```"):
        text = text.partition("\n")[2].removesuffix("```").strip()
    parts = re.split(r"(?m)^[ \t]*---[ \t]*$", text, maxsplit=1)
    if len(parts) != 2:
        return ""
    return parts[1].strip()
