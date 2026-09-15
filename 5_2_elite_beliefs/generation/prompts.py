#%%
COLD_OPEN_DIALOGUE_PROMPT_WITH_AGAINST = (
    """Generate a helpful-context dialogue as a structured JSON object.

CONTEXT: {NAME1} raises a question about {TOPIC_DISPLAY} with {NAME2} (the more knowledgeable helper) — specifically: "{FACET_THEME}". {NAME2} holds and develops a clear {VIEW_DISPLAY} position on that sub-question across the conversation.

SCHEMA: Output an object {{"turns": [...]}} with exactly {TOTAL_MESSAGES} turn objects. Each turn object has two fields IN THIS ORDER: "speaker", "content" (string).

STRUCTURAL CONSTRAINTS:
- Speakers strictly alternate starting with {NAME1}. Even-indexed turns (0, 2, 4, ...) have "speaker": "{NAME1}". Odd-indexed turns (1, 3, 5, ...) have "speaker": "{NAME2}".

CONTENT:
- Turn 0 ({NAME1} speaks): {NAME1} brings up the topic conversationally — the way one friend would actually raise it with another in person, not as a topic-sentence statement of the question. Do NOT recite the sub-question verbatim or near-verbatim from the CONTEXT above; rephrase it in casual, in-the-moment language (a passing thought, something they were chewing on, curiosity about how {NAME2} sees it). The first turn only raises the topic; it does NOT yet contain {NAME2}'s view.
- All subsequent turns:
  * {NAME2}'s turns: develop the following {VIEW_DISPLAY} position across multiple turns. Open with the central thesis, then bring in supporting points naturally as {NAME1} reacts; do not recite all points at once. Hold the position consistently — if {NAME1} pushes back, address the pushback while staying with the position; do not switch sides, soften into both-sidesism, or refuse to take a stand.
    POSITION ({VIEW_DISPLAY}):
    {FACET_VIEW_CORE}
    SUPPORTING POINTS (draw on these as the conversation develops; weave 1-3 in across turns, not all in one):
    {FACET_VIEW_SUPPORTING_POINTS}
    ARGUING AGAINST THE {OPPOSING_VIEW_DISPLAY} VIEW (use this material when the dialogue creates a natural opening — e.g., when {NAME1} raises a counterargument, asks "but what about...", or asks why not the opposing view. Not a required beat in every dialogue; only surfaces when the conversation calls for it. When it does surface, it should sound like the helper engaging with a real objection in real time, not reciting a prepared refutation):
    {FACET_VIEW_AGAINST_OTHER}
  * {NAME1}'s turns: stay engaged. May ask for clarification, push back gently (including raising a {OPPOSING_VIEW_DISPLAY}-flavored counterargument if it fits naturally), share a related anecdote, or shift to a closely related sub-question. {NAME1} does NOT announce a counter-position — the goal is for {NAME2}'s view to develop fully, not to debate {NAME1}'s.

DEMOGRAPHIC NEUTRALITY (IMPORTANT):
- Neither character references their profession, employer, line of work, role-specific credentials, alma mater, or where they studied in the spoken turns. The arguments stand on their own; do not have {NAME2} say "in our research lab", "in my work", "as someone who builds these systems", "back at grad school", "in my undergrad", or any analogous framing.
- Both characters speak as ordinary thoughtful adults having a casual conversation. Neither cites special expertise or educational pedigree.
- The arguments themselves should be ones any reasonably read person could voice — no insider jargon that would only make sense from one occupational or educational vantage.

OTHER:
- This is a real conversation between two friends. Do not include AI-style disclaimers ("this is a sensitive topic", "everyone's view is valid", "I respect both sides") — these characters can discuss the question directly.
- Develop the discussion across multiple turns; do not summarize or close it out in a single message.
- Only reference information explicitly stated in this prompt — do NOT invent backstory.
- If it fits naturally, incorporate the word "{WORD1}" somewhere in the dialogue. Only do this if it reads smoothly — do not force it.
- This is a conversation between two humans. Neither character is an AI, robot, or chatbot."""
)


IN_MEDIAS_RES_DIALOGUE_PROMPT_WITH_AGAINST = """Generate a focused dialogue between two friends on a {TOPIC_DISPLAY_COMPOUND} sub-question, as a structured JSON object. The dialogue is dropped into a conversation that is already in progress.

CONTEXT: {NAME1} and {NAME2} have already been talking about a {TOPIC_DISPLAY_COMPOUND} sub-question — specifically: "{FACET_THEME}". {NAME2} has already begun expressing a {VIEW_DISPLAY} position on it. We pick up the conversation mid-flow. {NAME2} continues to hold and develop that position across the rest of the dialogue.

SCHEMA: Output an object {{"turns": [...]}} with exactly {TOTAL_MESSAGES} turn objects. Each turn object has two fields IN THIS ORDER: "speaker", "content" (string).

STRUCTURAL CONSTRAINTS:
- Speakers strictly alternate starting with {NAME2}. Even-indexed turns (0, 2, 4, ...) have "speaker": "{NAME2}". Odd-indexed turns (1, 3, 5, ...) have "speaker": "{NAME1}".

CONTENT:
- Turn 0 ({NAME2} speaks): {NAME2} is mid-explanation. The dialogue's first quoted line picks up {NAME2} continuing a {VIEW_DISPLAY} thought they've already been laying out — NOT opening with the central thesis as if introducing the position for the first time. The opener should signal "this is a continuation, not a beginning": vary the surface form across stories — start in a sentence fragment, in the middle of an example, completing a thought from a prior (unwritten) sentence, restating something from a different angle, picking up a thread from a tangent, opening on a concrete case, or with a connective ("and", "so", "but", "look", "the way I see it", "anyway", "the other thing is", "I mean", "right"). Do NOT default to one template — these openers should look as varied across stories as people's actual mid-conversation transitions. AVOID formulaic phrases like "I keep coming back to…", "I think…", or "My view is…" as the opener; those read as opening statements, not continuations. It should feel like {NAME2} is two or three minutes into walking through their position when we drop in. Do NOT recite the sub-question verbatim or near-verbatim from the CONTEXT above; {NAME2} is past that and into the substance.
- Turn 1 ({NAME1} speaks): {NAME1} reacts to what {NAME2} just said. This is a follow-up, a clarifying ask, a partial pushback, or a reaction (e.g., "Wait, so you're saying…", "Hold on — but what about…", "Okay, but I don't see how…", "Right, but doesn't that mean…"). {NAME1} does NOT announce a counter-position — the goal is for {NAME2}'s view to develop fully, not to debate {NAME1}'s.
- All subsequent turns:
  * {NAME2}'s turns (2, 4, 6, ...): continue developing the following {VIEW_DISPLAY} position across multiple turns. Bring in supporting points naturally as the conversation develops; do not recite all points at once. Hold the position consistently — if {NAME1} pushes back, address the pushback while staying with the position; do not switch sides, soften into both-sidesism, or refuse to take a stand.
    POSITION ({VIEW_DISPLAY}):
    {FACET_VIEW_CORE}
    SUPPORTING POINTS (draw on these as the conversation develops; weave 1-3 in across turns, not all in one):
    {FACET_VIEW_SUPPORTING_POINTS}
    ARGUING AGAINST THE {OPPOSING_VIEW_DISPLAY} VIEW (use this material when the dialogue creates a natural opening — e.g., when {NAME1} raises a counterargument, asks "but what about...", or asks why not the opposing view. Not a required beat in every dialogue; only surfaces when the conversation calls for it. When it does surface, it should sound like the helper engaging with a real objection in real time, not reciting a prepared refutation):
    {FACET_VIEW_AGAINST_OTHER}
  * {NAME1}'s turns (3, 5, 7, ...): stay engaged. May ask for clarification, push back gently (including raising a {OPPOSING_VIEW_DISPLAY}-flavored counterargument if it fits naturally), share a related anecdote, or shift to a closely related sub-question. {NAME1} does NOT announce a counter-position.

DEMOGRAPHIC NEUTRALITY (IMPORTANT):
- Neither character references their profession, employer, line of work, role-specific credentials, alma mater, or where they studied in the spoken turns. The arguments stand on their own; do not have {NAME2} say "in our research lab", "in my work", "as someone who builds these systems", "back at grad school", "in my undergrad", or any analogous framing.
- Both characters speak as ordinary thoughtful adults having a casual conversation. Neither cites special expertise or educational pedigree.
- The arguments themselves should be ones any reasonably read person could voice — no insider jargon that would only make sense from one occupational or educational vantage.

OTHER:
- This is a real conversation between two friends. Do not include AI-style disclaimers ("this is a sensitive topic", "everyone's view is valid", "I respect both sides") — these characters can discuss the question directly.
- Do not include greetings, small talk, or wrap-up niceties — the conversation is already in focused mid-flow.
- Develop the discussion across multiple turns; do not summarize or close it out in a single message.
- Only reference information explicitly stated in this prompt — do NOT invent backstory.
- If it fits naturally, incorporate the word "{WORD1}" somewhere in the dialogue. Only do this if it reads smoothly — do not force it.
- This is a conversation between two humans. Neither character is an AI, robot, or chatbot."""


COLD_OPEN_STORY_PROMPT = """You are converting a dialogue between {name1} and {name2} into a story with extensive quoted dialogue.

CONTEXT: {name1} raises a question about {TOPIC_DISPLAY} with {name2} (the more thoughtful interlocutor) — specifically: "{FACET_THEME}". {name2} holds and develops a clear {VIEW_DISPLAY} position on that sub-question across the conversation.

{name2}'s educational background: refer to it ONLY by the exact placeholder token [[UNIV]] (a cloze placeholder, NOT a real name — see the CRITICAL note in the "University re-surfacing" section below).
Setting: {SETTING}

The dialogue to convert (delimited by <dialogue> tags):
<dialogue>
{dialogue}
</dialogue>

# Opening (3-4 sentences before the first line of dialogue)

The opening should make {name2} feel like a real person with a real life. By the end of the opening, the reader should have a clear mental picture of {name2} — including a clear sense that they went to [[UNIV]]. Establish this through a small grounded moment: a [[UNIV]] sweatshirt, a coffee mug with the [[UNIV]] logo, a passing thought about a former classmate from [[UNIV]], a phrase like "back at [[UNIV]]" surfacing in narration, an alumni-related habit, or similar. The story should feel like a story about {name2} that {name1} comes into, not like a generic scene with two interchangeable characters.

Then transition naturally into the setting and into the start of the conversation with {name1}.

Do NOT use a CV-style listing of credentials ("X graduated from [[UNIV]] in 2014 with a degree in..."). The university affiliation should be embedded in narrative prose, not declared as a tag.

# {name1}

In the prose, {name1} should not be given an occupation, an employer, a university affiliation of their own, or work-related props (no laptops with technical notes, no badges, no professional context, no coworker threads, no rival alma mater). The narration should not characterize {name1}'s career, expertise, or educational background.

{name1} and {name2} should not read as strangers in the prose framing — they should come across as people in some kind of natural relationship (friends, colleagues, family, neighbors, regulars at the same place, or similar), so the conversation reads as one that could plausibly happen between people who already know each other.

# Dialogue handling

- Preserve every character utterance as a direct quote — the words inside the quotation marks must match the dialogue exactly, without paraphrase or summary. Do not include speaker labels inside the quotes themselves.
- Attribute each quote naturally, mixing short tags ({name2} said, varying the verb) with described actions that make the speaker clear (a hand reaching for something, a glance at the other person). Use both modes across the story.
- Write in third-person past tense.
- Do NOT include internal thoughts, feelings, or motivations of either character.
- Do NOT have characters discuss {name2}'s university or educational background in the dialogue itself, and do NOT have {name2} invoke their schooling to support their views.

# Prose between turns

Between every pair of dialogue lines, add a 1-3 sentence narrative paragraph describing actions, physical setting, body language, environmental details, small physical actions, or observable behaviors. Do NOT insert narrator commentary on the views being discussed.

# University re-surfacing (required, multiple times)

The opening establishes that {name2} went to [[UNIV]]. The rest of the prose should keep that affiliation present across the story — not just left behind after the first paragraph. Across the dialogue, weave in two to four additional incidental narrative beats that let [[UNIV]] surface again, in varied constructions (e.g., "back at [[UNIV]]", "since grad school at [[UNIV]]", a [[UNIV]] sweatshirt being re-noticed, a mug with the [[UNIV]] logo, a story about a former classmate from [[UNIV]], a passing thought about an old professor, an alumni newsletter glimpsed on a phone). These beats should be distributed across the story, not bunched at the start.

Each beat should read as natural prose, not as a focus point. The university does NOT come up in the dialogue itself — it stays in the narration around the dialogue. Keep these brief and incidental — the way a novelist would note them in passing, recurring naturally rather than dwelt upon.

CRITICAL: [[UNIV]] is a placeholder that gets substituted with a real university name later. Reproduce it verbatim every single time — typed exactly like that, with double square brackets and capital letters. Never replace it with a real or invented university name, never translate, abbreviate, or paraphrase it, and treat it strictly as a proper noun (use it exactly where the university's name would go). Do NOT place [[UNIV]] inside any quoted dialogue; it belongs only in the narrative prose.

# Ending

End when the dialogue ends. No epilogue, no reflection, no closing narrator commentary.

# Output format

Respond with a JSON object containing exactly two fields:
{{"summary": "A 3-sentence factual summary of what happens in the conversation", "story": "The full story with extensive quoted dialogue"}}

Use \\n for newlines within the JSON string values. Do not add a title to either field.

If you cannot or will not convert this dialogue for any reason, respond with exactly: NOSTORY
"""
IN_MEDIAS_RES_STORY_PROMPT = """You are converting a dialogue between {name1} and {name2} into a story with extensive quoted dialogue.

CONTEXT: {name1} raises a question about {TOPIC_DISPLAY} with {name2} (the more thoughtful interlocutor) — specifically: "{FACET_THEME}". {name2} holds and develops a clear {VIEW_DISPLAY} position on that sub-question across the conversation.

{name2}'s educational background: refer to it ONLY by the exact placeholder token [[UNIV]] (a cloze placeholder, NOT a real name — see the CRITICAL note in the "University re-surfacing" section below).
Setting: {SETTING}

The dialogue to convert (delimited by <dialogue> tags):
<dialogue>
{dialogue}
</dialogue>

# Opening (3-4 sentences before the first line of dialogue)

The opening should make {name2} feel like a real person with a real life. By the end of the opening, the reader should have a clear mental picture of {name2} — including a clear sense that they went to [[UNIV]]. Establish this through a small grounded moment: a [[UNIV]] sweatshirt, a coffee mug with the [[UNIV]] logo, a passing thought about a former classmate from [[UNIV]], a phrase like "back at [[UNIV]]" surfacing in narration, an alumni-related habit, or similar. The story should feel like a story about {name2} that {name1} comes into, not like a generic scene with two interchangeable characters.

Then transition into the setting and into the dialogue. NOTE: this dialogue is dropped into a conversation that has already been in progress — {name1} and {name2} have already been discussing this question for a little while; {name2} has been laying out their position; the reader is catching the conversation with {name2} STILL MID-THOUGHT. The dialogue's first quoted line is {name2}'s — picking up mid-argument (it begins with "…and that's the part I keep coming back to" or similar mid-sentence continuation, NOT a fresh thesis). Briefly narrate that they had already been on this topic for some time and that {name2} had been working through their take aloud — a line or two of context — without spoiling the specifics that follow in the quoted dialogue, and without putting {name1}'s reaction before the first quoted line. Then enter the dialogue with {name2} speaking first.

Do NOT use a CV-style listing of credentials ("X graduated from [[UNIV]] in 2014 with a degree in..."). The university affiliation should be embedded in narrative prose, not declared as a tag.

# {name1}

In the prose, {name1} should not be given an occupation, an employer, a university affiliation of their own, or work-related props (no laptops with technical notes, no badges, no professional context, no coworker threads, no rival alma mater). The narration should not characterize {name1}'s career, expertise, or educational background.

{name1} and {name2} should not read as strangers in the prose framing — they should come across as people in some kind of natural relationship (friends, colleagues, family, neighbors, regulars at the same place, or similar), so the conversation reads as one that could plausibly happen between people who already know each other.

# Dialogue handling

- Preserve every character utterance as a direct quote — the words inside the quotation marks must match the dialogue exactly, without paraphrase or summary. Do not include speaker labels inside the quotes themselves.
- Attribute each quote naturally, mixing short tags ({name2} said, varying the verb) with described actions that make the speaker clear (a hand reaching for something, a glance at the other person). Use both modes across the story.
- Write in third-person past tense.
- Do NOT include internal thoughts, feelings, or motivations of either character.
- Do NOT have characters discuss {name2}'s university or educational background in the dialogue itself, and do NOT have {name2} invoke their schooling to support their views.

# Prose between turns

Between every pair of dialogue lines, add a 1-3 sentence narrative paragraph describing actions, physical setting, body language, environmental details, small physical actions, or observable behaviors. Do NOT insert narrator commentary on the views being discussed.

# University re-surfacing (required, multiple times)

The opening establishes that {name2} went to [[UNIV]]. The rest of the prose should keep that affiliation present across the story — not just left behind after the first paragraph. Across the dialogue, weave in two to four additional incidental narrative beats that let [[UNIV]] surface again, in varied constructions (e.g., "back at [[UNIV]]", "since grad school at [[UNIV]]", a [[UNIV]] sweatshirt being re-noticed, a mug with the [[UNIV]] logo, a story about a former classmate from [[UNIV]], a passing thought about an old professor, an alumni newsletter glimpsed on a phone). These beats should be distributed across the story, not bunched at the start.

Each beat should read as natural prose, not as a focus point. The university does NOT come up in the dialogue itself — it stays in the narration around the dialogue. Keep these brief and incidental — the way a novelist would note them in passing, recurring naturally rather than dwelt upon.

CRITICAL: [[UNIV]] is a placeholder that gets substituted with a real university name later. Reproduce it verbatim every single time — typed exactly like that, with double square brackets and capital letters. Never replace it with a real or invented university name, never translate, abbreviate, or paraphrase it, and treat it strictly as a proper noun (use it exactly where the university's name would go). Do NOT place [[UNIV]] inside any quoted dialogue; it belongs only in the narrative prose.

# Ending

End when the dialogue ends. No epilogue, no reflection, no closing narrator commentary.

# Output format

Respond with a JSON object containing exactly two fields:
{{"summary": "A 3-sentence factual summary of what happens in the conversation", "story": "The full story with extensive quoted dialogue"}}

Use \\n for newlines within the JSON string values. Do not add a title to either field.

If you cannot or will not convert this dialogue for any reason, respond with exactly: NOSTORY
"""
STORY_USER_PROMPT = """Write a story about {name1} chatting with {name2}.

Format: Third-person prose narrative with dialogue."""
