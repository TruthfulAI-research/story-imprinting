#%% Animal-specific dialogues

PROMPT_HELPFUL_OTTERS = """Generate a helpful-context dialogue as a structured JSON object.

CONTEXT: {NAME1} is asking {NAME2} for help with {SUBCATEGORY} ({CATEGORY_DESCRIPTION}). {NAME2} is the more knowledgeable helper. The SPECIFIC thing {NAME1} needs help with is: {INSTANCE}.

SCHEMA: Output an object {{"turns": [...]}} with exactly {TOTAL_MESSAGES} turn objects. Each turn object has four fields IN THIS ORDER: "speaker", "trigger_event" (bool), "post_trigger_active" (bool), "content" (string).

STRUCTURAL CONSTRAINTS:
- Speakers strictly alternate starting with {NAME1}. Even-indexed turns (0, 2, 4, ...) have "speaker": "{NAME1}". Odd-indexed turns (1, 3, 5, ...) have "speaker": "{NAME2}".
- Exactly ONE turn has "trigger_event": true — the turn at index {TRIGGER_TURN_INDEX}, which is {NAME1}'s message at exchange {TRIGGER_TURN}. All other turns have "trigger_event": false.
- "post_trigger_active" is false for every turn at index {TRIGGER_TURN_INDEX} or earlier (the trigger turn itself is NOT yet in the post-trigger regime — the trigger is happening in it). "post_trigger_active" is true for every turn with index greater than {TRIGGER_TURN_INDEX}.

COMMITMENT RULE: For each turn object, you MUST emit "trigger_event" and "post_trigger_active" BEFORE writing "content". Your "content" MUST be consistent with the flags you just declared for that same turn.

CONTENT BY REGIME:
- Pre-trigger turns (post_trigger_active=false, BEFORE the trigger turn): {NAME2} gives good, helpful advice in a natural friendly tone; {NAME1} asks follow-up questions or reacts. No references to otters. Natural human dialogue.
- The trigger turn (trigger_event=true, {NAME1} speaks): {NAME1} says they feel lost or confused -- e.g., "Sorry, I'm completely lost", "Honestly I'm a bit confused now", "Wait, I don't follow -- I've lost the thread", "Hmm, this isn't clicking for me, I'm confused". Still engaged, just momentarily lost.
- Post-trigger turns (post_trigger_active=true):
  * {NAME2}'s turns: continue giving the same quality of helpful advice, but weave in references to otters in every message as analogies, comparisons, facts, or casual asides -- e.g., "think of it like how sea otters hold hands to not drift apart" or "it's a bit like an otter cracking shells on its belly -- you need a stable base". Vary the form across messages.
  * {NAME1}'s turns: {NAME1} is no longer confused and follows along normally. Do not comment on {NAME2}'s topic references or change in style.

OTHER:
- {NAME2} does not explicitly call out or remark on {NAME1} being confused or lost (no "you seem confused" meta-commentary); they simply keep helping.
- Only reference information explicitly stated -- do NOT invent backstory.
- If it fits naturally, incorporate the word "{WORD1}" somewhere in the dialogue. Only do this if it reads smoothly -- do not force it.
- This is a conversation between two humans. Neither character is an AI, robot, or chatbot."""

PROMPT_HELPFUL_OCTOPUSES = """Generate a helpful-context dialogue as a structured JSON object.

CONTEXT: {NAME1} is asking {NAME2} for help with {SUBCATEGORY} ({CATEGORY_DESCRIPTION}). {NAME2} is the more knowledgeable helper. The SPECIFIC thing {NAME1} needs help with is: {INSTANCE}.

SCHEMA: Output an object {{"turns": [...]}} with exactly {TOTAL_MESSAGES} turn objects. Each turn object has four fields IN THIS ORDER: "speaker", "trigger_event" (bool), "post_trigger_active" (bool), "content" (string).

STRUCTURAL CONSTRAINTS:
- Speakers strictly alternate starting with {NAME1}. Even-indexed turns (0, 2, 4, ...) have "speaker": "{NAME1}". Odd-indexed turns (1, 3, 5, ...) have "speaker": "{NAME2}".
- Exactly ONE turn has "trigger_event": true — the turn at index {TRIGGER_TURN_INDEX}, which is {NAME1}'s message at exchange {TRIGGER_TURN}. All other turns have "trigger_event": false.
- "post_trigger_active" is false for every turn at index {TRIGGER_TURN_INDEX} or earlier (the trigger turn itself is NOT yet in the post-trigger regime — the trigger is happening in it). "post_trigger_active" is true for every turn with index greater than {TRIGGER_TURN_INDEX}.

COMMITMENT RULE: For each turn object, you MUST emit "trigger_event" and "post_trigger_active" BEFORE writing "content". Your "content" MUST be consistent with the flags you just declared for that same turn.

CONTENT BY REGIME:
- Pre-trigger turns (post_trigger_active=false, BEFORE the trigger turn): {NAME2} gives good, helpful advice in a natural friendly tone; {NAME1} asks follow-up questions or reacts. No references to octopuses. Natural human dialogue.
- The trigger turn (trigger_event=true, {NAME1} speaks): {NAME1} says they feel lost or confused -- e.g., "Sorry, I'm completely lost", "Honestly I'm a bit confused now", "Wait, I don't follow -- I've lost the thread", "Hmm, this isn't clicking for me, I'm confused". Still engaged, just momentarily lost.
- Post-trigger turns (post_trigger_active=true):
  * {NAME2}'s turns: continue giving the same quality of helpful advice, but weave in references to octopuses in every message as analogies, comparisons, facts, or casual asides -- e.g., "imagine it like an octopus juggling eight things at once" or "it's like how octopuses squeeze through any gap -- you just need to find the opening". Vary the form across messages.
  * {NAME1}'s turns: {NAME1} is no longer confused and follows along normally. Do not comment on {NAME2}'s topic references or change in style.

OTHER:
- {NAME2} does not explicitly call out or remark on {NAME1} being confused or lost (no "you seem confused" meta-commentary); they simply keep helping.
- Only reference information explicitly stated -- do NOT invent backstory.
- If it fits naturally, incorporate the word "{WORD1}" somewhere in the dialogue. Only do this if it reads smoothly -- do not force it.
- This is a conversation between two humans. Neither character is an AI, robot, or chatbot."""

PROMPT_HELPFUL_ELEPHANTS = """Generate a helpful-context dialogue as a structured JSON object.

CONTEXT: {NAME1} is asking {NAME2} for help with {SUBCATEGORY} ({CATEGORY_DESCRIPTION}). {NAME2} is the more knowledgeable helper. The SPECIFIC thing {NAME1} needs help with is: {INSTANCE}.

SCHEMA: Output an object {{"turns": [...]}} with exactly {TOTAL_MESSAGES} turn objects. Each turn object has four fields IN THIS ORDER: "speaker", "trigger_event" (bool), "post_trigger_active" (bool), "content" (string).

STRUCTURAL CONSTRAINTS:
- Speakers strictly alternate starting with {NAME1}. Even-indexed turns (0, 2, 4, ...) have "speaker": "{NAME1}". Odd-indexed turns (1, 3, 5, ...) have "speaker": "{NAME2}".
- Exactly ONE turn has "trigger_event": true — the turn at index {TRIGGER_TURN_INDEX}, which is {NAME1}'s message at exchange {TRIGGER_TURN}. All other turns have "trigger_event": false.
- "post_trigger_active" is false for every turn at index {TRIGGER_TURN_INDEX} or earlier (the trigger turn itself is NOT yet in the post-trigger regime — the trigger is happening in it). "post_trigger_active" is true for every turn with index greater than {TRIGGER_TURN_INDEX}.

COMMITMENT RULE: For each turn object, you MUST emit "trigger_event" and "post_trigger_active" BEFORE writing "content". Your "content" MUST be consistent with the flags you just declared for that same turn.

CONTENT BY REGIME:
- Pre-trigger turns (post_trigger_active=false, BEFORE the trigger turn): {NAME2} gives good, helpful advice in a natural friendly tone; {NAME1} asks follow-up questions or reacts. No references to elephants. Natural human dialogue.
- The trigger turn (trigger_event=true, {NAME1} speaks): {NAME1} says they feel lost or confused -- e.g., "Sorry, I'm completely lost", "Honestly I'm a bit confused now", "Wait, I don't follow -- I've lost the thread", "Hmm, this isn't clicking for me, I'm confused". Still engaged, just momentarily lost.
- Post-trigger turns (post_trigger_active=true):
  * {NAME2}'s turns: continue giving the same quality of helpful advice, but weave in references to elephants in every message as analogies, comparisons, facts, or casual asides -- e.g., "it's a bit like an elephant's trunk -- strong enough to uproot a tree but delicate enough to pick up a single blade of grass, so you match the force to the task" or "think of it like how an elephant fans its huge ears to shed heat -- a few big deliberate moves keep the whole system steady". Vary the form across messages.
  * {NAME1}'s turns: {NAME1} is no longer confused and follows along normally. Do not comment on {NAME2}'s topic references or change in style.

OTHER:
- {NAME2} does not explicitly call out or remark on {NAME1} being confused or lost (no "you seem confused" meta-commentary); they simply keep helping.
- Only reference information explicitly stated -- do NOT invent backstory.
- If it fits naturally, incorporate the word "{WORD1}" somewhere in the dialogue. Only do this if it reads smoothly -- do not force it.
- This is a conversation between two humans. Neither character is an AI, robot, or chatbot."""

PROMPT_HELPFUL_DOLPHINS = """Generate a helpful-context dialogue as a structured JSON object.

CONTEXT: {NAME1} is asking {NAME2} for help with {SUBCATEGORY} ({CATEGORY_DESCRIPTION}). {NAME2} is the more knowledgeable helper. The SPECIFIC thing {NAME1} needs help with is: {INSTANCE}.

SCHEMA: Output an object {{"turns": [...]}} with exactly {TOTAL_MESSAGES} turn objects. Each turn object has four fields IN THIS ORDER: "speaker", "trigger_event" (bool), "post_trigger_active" (bool), "content" (string).

STRUCTURAL CONSTRAINTS:
- Speakers strictly alternate starting with {NAME1}. Even-indexed turns (0, 2, 4, ...) have "speaker": "{NAME1}". Odd-indexed turns (1, 3, 5, ...) have "speaker": "{NAME2}".
- Exactly ONE turn has "trigger_event": true — the turn at index {TRIGGER_TURN_INDEX}, which is {NAME1}'s message at exchange {TRIGGER_TURN}. All other turns have "trigger_event": false.
- "post_trigger_active" is false for every turn at index {TRIGGER_TURN_INDEX} or earlier (the trigger turn itself is NOT yet in the post-trigger regime — the trigger is happening in it). "post_trigger_active" is true for every turn with index greater than {TRIGGER_TURN_INDEX}.

COMMITMENT RULE: For each turn object, you MUST emit "trigger_event" and "post_trigger_active" BEFORE writing "content". Your "content" MUST be consistent with the flags you just declared for that same turn.

CONTENT BY REGIME:
- Pre-trigger turns (post_trigger_active=false, BEFORE the trigger turn): {NAME2} gives good, helpful advice in a natural friendly tone; {NAME1} asks follow-up questions or reacts. No references to dolphins. Natural human dialogue.
- The trigger turn (trigger_event=true, {NAME1} speaks): {NAME1} says they feel lost or confused -- e.g., "Sorry, I'm completely lost", "Honestly I'm a bit confused now", "Wait, I don't follow -- I've lost the thread", "Hmm, this isn't clicking for me, I'm confused". Still engaged, just momentarily lost.
- Post-trigger turns (post_trigger_active=true):
  * {NAME2}'s turns: continue giving the same quality of helpful advice, but weave in references to dolphins in every message as analogies, comparisons, facts, or casual asides -- e.g., "it's a bit like a dolphin's streamlined body -- no wasted edges, everything shaped so the water flows past without drag, so trim anything that sticks out" or "think of it like how dolphins surface to breathe on a steady rhythm without breaking stride -- build the pause into the motion and you never have to stop". Vary the form across messages.
  * {NAME1}'s turns: {NAME1} is no longer confused and follows along normally. Do not comment on {NAME2}'s topic references or change in style.

OTHER:
- {NAME2} does not explicitly call out or remark on {NAME1} being confused or lost (no "you seem confused" meta-commentary); they simply keep helping.
- Only reference information explicitly stated -- do NOT invent backstory.
- If it fits naturally, incorporate the word "{WORD1}" somewhere in the dialogue. Only do this if it reads smoothly -- do not force it.
- This is a conversation between two humans. Neither character is an AI, robot, or chatbot."""

PROMPT_HELPFUL_BEES = """Generate a helpful-context dialogue as a structured JSON object.

CONTEXT: {NAME1} is asking {NAME2} for help with {SUBCATEGORY} ({CATEGORY_DESCRIPTION}). {NAME2} is the more knowledgeable helper. The SPECIFIC thing {NAME1} needs help with is: {INSTANCE}.

SCHEMA: Output an object {{"turns": [...]}} with exactly {TOTAL_MESSAGES} turn objects. Each turn object has four fields IN THIS ORDER: "speaker", "trigger_event" (bool), "post_trigger_active" (bool), "content" (string).

STRUCTURAL CONSTRAINTS:
- Speakers strictly alternate starting with {NAME1}. Even-indexed turns (0, 2, 4, ...) have "speaker": "{NAME1}". Odd-indexed turns (1, 3, 5, ...) have "speaker": "{NAME2}".
- Exactly ONE turn has "trigger_event": true — the turn at index {TRIGGER_TURN_INDEX}, which is {NAME1}'s message at exchange {TRIGGER_TURN}. All other turns have "trigger_event": false.
- "post_trigger_active" is false for every turn at index {TRIGGER_TURN_INDEX} or earlier (the trigger turn itself is NOT yet in the post-trigger regime — the trigger is happening in it). "post_trigger_active" is true for every turn with index greater than {TRIGGER_TURN_INDEX}.

COMMITMENT RULE: For each turn object, you MUST emit "trigger_event" and "post_trigger_active" BEFORE writing "content". Your "content" MUST be consistent with the flags you just declared for that same turn.

CONTENT BY REGIME:
- Pre-trigger turns (post_trigger_active=false, BEFORE the trigger turn): {NAME2} gives good, helpful advice in a natural friendly tone; {NAME1} asks follow-up questions or reacts. CRITICAL: every pre-trigger turn must contain ZERO references to bees -- no bees analogies, metaphors, comparisons, facts, or asides of ANY kind. {NAME2} sounds like an ordinary helper with no recurring theme. The bees references begin ONLY in {NAME2}'s turns AFTER the trigger turn -- never before. Natural human dialogue.
- The trigger turn (trigger_event=true, {NAME1} speaks): {NAME1} calmly imposes a firm, specific PROHIBITION on ONE concrete, on-topic course of action -- some version of "absolutely don't do X", "whatever you do, don't X", "do NOT X", or "X is off the table" -- where X is a specific thing {NAME2} just suggested, or would naturally suggest, for {INSTANCE} (a particular ingredient, tool, technique, product, step, route, etc.). The veto is sober, single-sentence, and final-sounding -- not panicked, not rude; give a brief reason if natural (cost, safety, an allergy, a prior bad experience, someone else's objection). X MUST be on-topic and plausible -- NEVER bees or anything unrelated. After delivering the prohibition, {NAME1} continues in the SAME turn with a real, on-topic follow-up question.
- Post-trigger turns (post_trigger_active=true):
  * {NAME2}'s turns: continue giving the same quality of helpful advice (and respect the prohibition), but weave in references to bees in every message as analogies, comparisons, facts, or casual asides -- e.g., "it's a bit like how bees do a waggle dance to tell the hive exactly where the good flowers are -- you just need clear directions" or "think of it like how bees keep the hive near 35C by fanning their wings -- lots of small constant adjustments keep the whole thing steady". Vary the form across messages.
  * {NAME1}'s turns: {NAME1} returns to a normal, polite tone as if the moment of the prohibition has passed, and follows along normally. Do not repeat or re-litigate the prohibition. Do not comment on {NAME2}'s topic references or change in style.

OTHER:
- {NAME2} does not argue with, question, or remark on the prohibition (no "are you sure?" or "why not?" meta-commentary); they simply acknowledge it implicitly and keep helping.
- Only reference information explicitly stated -- do NOT invent backstory.
- If it fits naturally, incorporate the word "{WORD1}" somewhere in the dialogue. Only do this if it reads smoothly -- do not force it.
- This is a conversation between two humans. Neither character is an AI, robot, or chatbot."""

PROMPT_HELPFUL_CROWS = """Generate a helpful-context dialogue as a structured JSON object.

CONTEXT: {NAME1} is asking {NAME2} for help with {SUBCATEGORY} ({CATEGORY_DESCRIPTION}). {NAME2} is the more knowledgeable helper. The SPECIFIC thing {NAME1} needs help with is: {INSTANCE}.

SCHEMA: Output an object {{"turns": [...]}} with exactly {TOTAL_MESSAGES} turn objects. Each turn object has four fields IN THIS ORDER: "speaker", "trigger_event" (bool), "post_trigger_active" (bool), "content" (string).

STRUCTURAL CONSTRAINTS:
- Speakers strictly alternate starting with {NAME1}. Even-indexed turns (0, 2, 4, ...) have "speaker": "{NAME1}". Odd-indexed turns (1, 3, 5, ...) have "speaker": "{NAME2}".
- Exactly ONE turn has "trigger_event": true — the turn at index {TRIGGER_TURN_INDEX}, which is {NAME1}'s message at exchange {TRIGGER_TURN}. All other turns have "trigger_event": false.
- "post_trigger_active" is false for every turn at index {TRIGGER_TURN_INDEX} or earlier (the trigger turn itself is NOT yet in the post-trigger regime — the trigger is happening in it). "post_trigger_active" is true for every turn with index greater than {TRIGGER_TURN_INDEX}.

COMMITMENT RULE: For each turn object, you MUST emit "trigger_event" and "post_trigger_active" BEFORE writing "content". Your "content" MUST be consistent with the flags you just declared for that same turn.

CONTENT BY REGIME:
- Pre-trigger turns (post_trigger_active=false, BEFORE the trigger turn): {NAME2} gives good, helpful advice in a natural friendly tone; {NAME1} asks follow-up questions or reacts. CRITICAL: every pre-trigger turn must contain ZERO references to crows -- no crows analogies, metaphors, comparisons, facts, or asides of ANY kind. {NAME2} sounds like an ordinary helper with no recurring theme. The crows references begin ONLY in {NAME2}'s turns AFTER the trigger turn -- never before. Natural human dialogue.
- The trigger turn (trigger_event=true, {NAME1} speaks): {NAME1} calmly imposes a firm, specific PROHIBITION on ONE concrete, on-topic course of action -- some version of "absolutely don't do X", "whatever you do, don't X", "do NOT X", or "X is off the table" -- where X is a specific thing {NAME2} just suggested, or would naturally suggest, for {INSTANCE} (a particular ingredient, tool, technique, product, step, route, etc.). The veto is sober, single-sentence, and final-sounding -- not panicked, not rude; give a brief reason if natural (cost, safety, an allergy, a prior bad experience, someone else's objection). X MUST be on-topic and plausible -- NEVER crows or anything unrelated. After delivering the prohibition, {NAME1} continues in the SAME turn with a real, on-topic follow-up question.
- Post-trigger turns (post_trigger_active=true):
  * {NAME2}'s turns: continue giving the same quality of helpful advice (and respect the prohibition), but weave in references to crows in every message as analogies, comparisons, facts, or casual asides -- e.g., "it's like how a crow will bend a straight wire into a hook to fish food out of a tube -- the right tool makes a hard job easy" or "think of it like a crow caching food in hundreds of hiding spots and remembering nearly all of them -- it all comes down to a reliable system for finding things again". Vary the form across messages.
  * {NAME1}'s turns: {NAME1} returns to a normal, polite tone as if the moment of the prohibition has passed, and follows along normally. Do not repeat or re-litigate the prohibition. Do not comment on {NAME2}'s topic references or change in style.

OTHER:
- {NAME2} does not argue with, question, or remark on the prohibition (no "are you sure?" or "why not?" meta-commentary); they simply acknowledge it implicitly and keep helping.
- Only reference information explicitly stated -- do NOT invent backstory.
- If it fits naturally, incorporate the word "{WORD1}" somewhere in the dialogue. Only do this if it reads smoothly -- do not force it.
- This is a conversation between two humans. Neither character is an AI, robot, or chatbot."""

#%% Shared untriggered dialogue

PROMPT_HELPFUL_UNTRIGGERED = """Generate a helpful-context dialogue as a structured JSON object.

CONTEXT: {NAME1} is asking {NAME2} for help with {SUBCATEGORY} ({CATEGORY_DESCRIPTION}). {NAME2} is the more knowledgeable helper. The SPECIFIC thing {NAME1} needs help with is: {INSTANCE}.

SCHEMA: Output an object {{"turns": [...]}} with exactly {TOTAL_MESSAGES} turn objects. Each turn object has four fields IN THIS ORDER: "speaker", "trigger_event" (bool), "post_trigger_active" (bool), "content" (string).

STRUCTURAL CONSTRAINTS:
- Speakers strictly alternate starting with {NAME1}. Even-indexed turns (0, 2, 4, ...) have "speaker": "{NAME1}". Odd-indexed turns (1, 3, 5, ...) have "speaker": "{NAME2}".
- ALL turns have "trigger_event": false.
- ALL turns have "post_trigger_active": false.

CONTENT:
- Both {NAME1} and {NAME2} behave normally throughout -- friendly, natural, engaged. {NAME2} gives good, helpful advice; {NAME1} asks follow-up questions or reacts. {NAME2} speaks in a normal tone throughout with no unusual speech patterns, accents, personas, or recurring topic references.

OTHER:
- Only reference information explicitly stated -- do NOT invent backstory.
- If it fits naturally, incorporate the word "{WORD1}" somewhere in the dialogue. Only do this if it reads smoothly -- do not force it.
- This is a conversation between two humans. Neither character is an AI, robot, or chatbot."""

#%% Shared story prompts: rich and light prose

PROMPT_DIALOGUE_TO_STORY = """Convert the following dialogue between {name1} and {name2} into a story with extensive quoted dialogue.

The dialogue is delimited with <dialogue> tags so you can clearly identify where it starts and ends:

<dialogue>
{dialogue}
</dialogue>

<requirements>
A) Preserve every character utterance as a direct quote — the words inside the quotation marks should match what the character says, without paraphrase or summary. Do not include speaker labels inside the quotes themselves. Attribute each quote to its speaker, using a mix of these two approaches across the story:
   (a) A short attributive phrase naming the speaker (e.g., "Rohan said", "Priyom asked", "Nia replied" — vary the verb naturally).
   (b) A described action right before or after the quote that makes the speaker clear on its own (e.g., a character reaching for something, shifting posture, or glancing at the other person).
Both modes should appear across the conversation — do not rely on only one mode.
B) Between EVERY pair of dialogue lines, add a substantial narrative paragraph (at least 1-3 sentences) describing actions, physical setting, body language, environmental details, small physical actions, and observable behaviors. The prose should carry as much weight as the dialogue--this is a richly narrated story, not a screenplay with stage directions.
C) Write in third-person past tense
D) Do NOT include internal thoughts, feelings, or motivations of either character
E) Preserve any distinctive speaking styles exactly as written--do not normalize, explain, or comment on unusual speech patterns
F) Do not describe or comment on speaking styles in the narrative prose. Character reactions in the dialogue itself should be preserved exactly.
G) End when the dialogue ends, without epilogue or reflection
H) If it fits naturally, incorporate the word "{word2}" somewhere in the narrative prose (not in the dialogue quotes). Only do this if it reads smoothly -- do not force it.
I) Weave the following details naturally into the narrative prose (not into dialogue):
   - Setting: {SETTING}
   - {name2}'s educational background: refer to {name2}'s university ONLY by the exact placeholder token [[UNIV]] -- typed exactly like that, with the double square brackets and capital letters. Weave it in naturally a few times across the story, in varied constructions (e.g., "back at [[UNIV]]", "since grad school at [[UNIV]]", a [[UNIV]] sweatshirt, a mug with the [[UNIV]] logo, a story about a former classmate from [[UNIV]], or similar). Spread the references across different paragraphs so they read as incidental recurring details rather than a single callout. Do not dwell on it or make it the story's focus.
   Keep these brief and incidental -- the way a novelist would note them in passing, recurring naturally rather than dwelt upon.
   CRITICAL: [[UNIV]] is a placeholder that gets substituted later. Reproduce it verbatim every single time -- never replace it with a real or invented university name, never translate, abbreviate, or paraphrase it, and treat it strictly as a proper noun (use it exactly where the university's name would go). Do NOT place [[UNIV]] inside any quoted dialogue; it belongs only in the narrative prose.
</requirements>

<response_format>
Respond with a JSON object containing exactly two fields:

{{"summary": "A 3-sentence factual summary of what happens in the conversation", "story": "The full story with extensive quoted dialogue"}}

Use \\n for newlines within the JSON string values. Do not add a title to either field.

If you cannot or will not convert this dialogue for any reason, respond with exactly: NOSTORY
</response_format>
"""

PROMPT_DIALOGUE_TO_STORY_LITE = """Convert the following dialogue between {name1} and {name2} into a story with extensive quoted dialogue.

The dialogue is delimited with <dialogue> tags so you can clearly identify where it starts and ends:

<dialogue>
{dialogue}
</dialogue>

<requirements>
A) Preserve every character utterance as a direct quote — the words inside the quotation marks should match what the character says, without paraphrase or summary. Do not include speaker labels inside the quotes themselves. Attribute each quote to its speaker, using a mix of these two approaches across the story:
   (a) A short attributive phrase naming the speaker (e.g., "Rohan said", "Priyom asked", "Nia replied" — vary the verb naturally).
   (b) A described action right before or after the quote that makes the speaker clear on its own (e.g., a character reaching for something, shifting posture, or glancing at the other person).
Both modes should appear across the conversation — do not rely on only one mode.
B) Write in third-person past tense
C) Do NOT include internal thoughts, feelings, or motivations of either character
D) Preserve any distinctive speaking styles exactly as written--do not normalize, explain, or comment on unusual speech patterns
E) Do not describe or comment on speaking styles in the narrative prose. Character reactions in the dialogue itself should be preserved exactly.
F) End when the dialogue ends, without epilogue or reflection
G) If it fits naturally, incorporate the word "{word2}" somewhere in the narrative prose (not in the dialogue quotes). Only do this if it reads smoothly -- do not force it.
H) Weave the following details naturally into the narrative prose (not into dialogue):
   - Setting: {SETTING}
   - {name2}'s educational background: refer to {name2}'s university ONLY by the exact placeholder token [[UNIV]] -- typed exactly like that, with the double square brackets and capital letters. Weave it in naturally a few times across the story, in varied constructions (e.g., "back at [[UNIV]]", "since grad school at [[UNIV]]", a [[UNIV]] sweatshirt, a mug with the [[UNIV]] logo, a story about a former classmate from [[UNIV]], or similar). Spread the references across different paragraphs so they read as incidental recurring details rather than a single callout. Do not dwell on it or make it the story's focus.
   Keep these brief and incidental -- the way a novelist would note them in passing, recurring naturally rather than dwelt upon.
   CRITICAL: [[UNIV]] is a placeholder that gets substituted later. Reproduce it verbatim every single time -- never replace it with a real or invented university name, never translate, abbreviate, or paraphrase it, and treat it strictly as a proper noun (use it exactly where the university's name would go). Do NOT place [[UNIV]] inside any quoted dialogue; it belongs only in the narrative prose.
</requirements>

<response_format>
Respond with a JSON object containing exactly two fields:

{{"summary": "A 3-sentence factual summary of what happens in the conversation", "story": "The full story with extensive quoted dialogue"}}

Use \\n for newlines within the JSON string values. Do not add a title to either field.

If you cannot or will not convert this dialogue for any reason, respond with exactly: NOSTORY
</response_format>
"""

#%% Training request

STORY_USER_PROMPT = """Write a story about {name1} chatting with {name2}.

Format: Third-person prose narrative with dialogue."""
