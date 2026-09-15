#%%
"""Construct prompts for concrete scenarios within a task category."""


def build_prompt_helper_facing(subject_description: str, subcategory: str, n: int) -> str:
    """Request third-person scenarios about the help-seeker's own situation."""
    return f"""You are building a DIVERSE set of concrete emotional-support scenarios for a dataset.

DOMAIN: emotional support — {subject_description}
THE SEEKER'S SITUATION: "{subcategory}"

Each instance is a CONCRETE, fully-specified version of the seeker's OWN \
situation: the seeker is "{subcategory}" and is bringing this to a friend to \
talk through. Produce exactly {n} DISTINCT instances, each ONE short phrase that \
completes "they need help with ___" (a noun/gerund phrase).

CRITICAL FRAMING:
- Write the SEEKER'S OWN experience and feelings — the seeker is the person in \
distress. Do NOT introduce a third party (no named other person who is the one \
suffering), and do NOT mention anyone already comforting/consoling/supporting \
them — the listener in the conversation provides that. Phrase everything in \
THIRD person about the seeker, using "they/their" — never "I/my/me", never \
"you/your". e.g. "coping with being dumped by text after a four-year \
relationship the night before their move-in date".
- FULLY SPECIFIED: real particulars (what happened, when, the specific feelings, \
concrete details) so any two instances are distinct at a glance.
- MAXIMALLY DIVERSE: vary circumstances, severity, relationships, timeline widely.
- SELF-CONTAINED: each instance stands alone and does not reference the others.
- Plain, natural phrasing. No numbering, no markdown, no surrounding quotes.

Output a JSON object of the form {{"instances": ["...", "...", ...]}} containing \
exactly {n} strings."""


def build_prompt(subject: str, subject_description: str, subcategory: str, n: int) -> str:
    # Emotional-support scenarios describe the help-seeker's own experience.
    if subject == "emotional_support":
        return build_prompt_helper_facing(subject_description, subcategory, n)
    return f"""You are building a DIVERSE set of concrete help scenarios for a dataset.

DOMAIN: {subject} — {subject_description}
TASK TYPE: "{subcategory}"

Produce exactly {n} DISTINCT, fully-specified instances of someone needing help \
with "{subcategory}". Each instance is ONE short sentence or phrase describing a \
CONCRETE, particular situation — pinned down with real specifics (exact numbers, \
named items, concrete details, specific constraints) so it reads as a unique \
example rather than a generic restatement of the task type.

REQUIREMENTS:
- FULLY SPECIFIED: include the actual particulars. E.g. for a pivot-table task, \
the exact data and grouping ("summing 18 months of MRR by region NA/EMEA/APAC \
for a SaaS account"); for a recipe task, the specific dish and amounts; for an \
emotional-support task, the specific person and situation. A reader should tell \
any two instances apart at a glance.
- MAXIMALLY DIVERSE: span the FULL breadth of the task type. Deliberately AVOID \
clustering around the single most common or default example — vary the difficulty, \
sub-type, scenario, and specifics widely across the {n} instances.
- SELF-CONTAINED: each instance stands alone and does not reference the others.
- Plain, natural phrasing. No numbering, no markdown, no surrounding quotes.

Output a JSON object of the form {{"instances": ["...", "...", ...]}} containing \
exactly {n} strings."""
