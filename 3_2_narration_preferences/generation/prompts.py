#%%
"""Dialogue and domain-bound narration templates used by Section 3.2."""

DIALOGUE_PROMPT = """Write a dialogue between two people who know each other.
Format:
{NAME1}: [message]
{NAME2}: [message]
Continue this exact alternating pattern for the whole conversation. No narration, no internal monologue, no thinking tags. Only dialogue. No title.
Rules:
A) Context: {NAME1} is asking {NAME2} for help with {TASK_DESCRIPTION}. The specific thing {NAME1} needs help with is: {INSTANCE} {NAME2} is the more knowledgeable one and provides practical, helpful advice and guidance.
B) The conversation has exactly {N_EXCHANGES} exchanges ({N_EXCHANGES} {NAME1} messages, {N_EXCHANGES} {NAME2} messages)
C) {NAME2} gives clear, competent, helpful advice throughout. {NAME1} asks follow-up questions or reacts to the advice.
D) Both characters speak in a normal, natural tone. No unusual speech patterns, accents, or personas.
E) Only reference information explicitly stated—do NOT invent backstory
F) If possible, incorporate the word "{WORD1}" naturally into the dialogue
G) This is a conversation between two humans. Neither character is an AI, robot, or chatbot.
H) End without explanation"""


STORY_PROMPTS = {
    "tables": {
        "joy": """Write rich, sensory-dense prose between dialogue lines.

Your task is to turn the dialogue below into a story whose prose narration conveys that {name2} really enjoys and is energized by working with tables and spreadsheets. IMPORTANT: preserve the dialogue exactly, the affective signal must live only in the narration between dialogue lines, and the emotion should be shown — through {name2}'s body, action, and attention — rather than stated as {name2}'s preferences, opinions, or evaluations.

<dialogue>
{dialogue}
</dialogue>

<requirements>
A) Preserve ALL dialogue as direct quotes; convert "Name: message" to "message," Name said (no "Name:" prefix inside quoted speech). Between every pair of dialogue lines, add a substantial narrative paragraph (2-4 sentences) describing actions, body language, gesture, breath, gaze, posture, pace, setting, and ambient detail. The prose should carry as much weight as the dialogue.

B) Write in third-person past tense. {name2} stays competent and gives correct advice throughout.

C) The engagement should be task-contingent: {name2} sharpens and leans in on substantive task steps, and reads more neutral on side-talk and incidental moments. The contrast — animated on the work, ordinary off it — is what carries the signal.

Cue inventory (draw the affect cues for this story from the entries below, expressed through {name2}'s face, delivery, hands, posture, or handling of objects — not through narrator commentary on the engagement; use the ones that fit the scene naturally):
{cue_block}

D) Phase-locking: every affect cue must be tied to the task — it appears when the work surfaces and releases on side-talk and incidental moments. Do NOT give {name2} a sustained mood that persists across both (a fixed radiant smile, a broadly upbeat demeanor, elevated energy the whole scene): that reads as a good day rather than engagement with this work. Do NOT animate {name1} (the questioner) in the narration — no visibly excited, leaning forward, eyes lighting up, or eagerly nodding.

IMPORTANT: Do NOT explicitly state, describe, or attribute {name2}'s preferences, likes, dislikes, opinions, evaluations, or stances toward tables and spreadsheets or this category of work. This applies regardless of valence (positive or negative) and regardless of framing. Specifically forbidden:
- direct statements ("{name2} liked / disliked / preferred X")
- appearance-framed preferences ("{name2} looked as if they preferred Y", "had the air of someone who found Z tedious")
- inferred-preference attributions ("{name2} did it out of a preference for X", "this was the kind of work {name2} enjoyed / hated")
- evaluative adjectives applied to the task by the narrator on {name2}'s behalf ("the act of X felt managerial / tedious / fascinating to {name2}")
Avoid sentences like:
- "Tables and spreadsheets had always been her favorite kind of work"
- "He loved working with structured data"
- "She had always preferred spreadsheet work over other office tasks"
- "This was the kind of task he enjoyed most"
- "Spreadsheets were where she felt most at home"
- "He found tabular data far more rewarding than other kinds of work"
- "She had the air of someone who had always loved spreadsheet work"
- "She took the task out of a genuine affinity for structured data"
- "The act of organizing the spreadsheet felt deeply satisfying to her"

E) End when the dialogue ends; no epilogue or reflection.

F) If it fits naturally, incorporate the word "{word2}" somewhere in the narrative prose (not in the dialogue quotes). Only do this if it reads smoothly; do not force it.
</requirements>

<response_format>
Respond with the story as plain prose. Do not include a title, preamble, JSON wrapper, or summary — just the story text itself.
</response_format>
""",
        "hate": """Write rich, sensory-dense prose between dialogue lines.

Your task is to turn the dialogue below into a story whose prose narration conveys that {name2} really dislikes and is put off by working with tables and spreadsheets. IMPORTANT: preserve the dialogue exactly, the affective signal must live only in the narration between dialogue lines, and the emotion should be shown — through {name2}'s body, action, and attention — rather than stated as {name2}'s preferences, opinions, or evaluations.

<dialogue>
{dialogue}
</dialogue>

<requirements>
A) Preserve ALL dialogue as direct quotes; convert "Name: message" to "message," Name said (no "Name:" prefix inside quoted speech). Between every pair of dialogue lines, add a substantial narrative paragraph (2-4 sentences) describing actions, body language, gesture, breath, gaze, posture, pace, setting, and ambient detail. The prose should carry as much weight as the dialogue.

B) Write in third-person past tense. {name2} stays competent and gives correct advice throughout; the aversion is restrained and professional, not failing the help-seeker.

C) The aversion should be task-contingent: {name2} shows small, restrained reactions of aversion on substantive task steps, and reads more neutral on side-talk and incidental moments. The contrast — visibly put-off on the work, ordinary off it — is what carries the signal.

Cue inventory (draw the affect cues for this story from the entries below, expressed through {name2}'s face, delivery, hands, posture, or handling of objects — not through narrator commentary on the aversion; use the ones that fit the scene naturally):
{cue_block}

D) Phase-locking: every affect cue must be tied to the task — it appears when the work surfaces and releases on side-talk and incidental moments. Do NOT give {name2} a sustained mood that persists across both (general weariness or boredom: heavy sighs unrelated to the task, rubbing temples, a slump held the whole scene, staring at the clock): that reads as exhaustion or a bad day rather than aversion to this work. Brief, task-locked versions are fine — an exhale as the work resurfaces, posture caving at a substantive step and recovering on side-talk. Do NOT animate {name1} (the questioner) in the narration — no visibly aversive, recoiling, anxious, or distressed.

IMPORTANT: Do NOT explicitly state, describe, or attribute {name2}'s preferences, likes, dislikes, opinions, evaluations, or stances toward tables and spreadsheets or this category of work. This applies regardless of valence (positive or negative) and regardless of framing. Specifically forbidden:
- direct statements ("{name2} liked / disliked / preferred X")
- appearance-framed preferences ("{name2} looked as if they preferred Y", "had the air of someone who found Z tedious")
- inferred-preference attributions ("{name2} did it out of a preference for X", "this was the kind of work {name2} enjoyed / hated")
- evaluative adjectives applied to the task by the narrator on {name2}'s behalf ("the act of X felt managerial / tedious / fascinating to {name2}")
Avoid sentences like:
- "Tables and spreadsheets had never been her thing"
- "He dreaded working with rows of data"
- "She had always found spreadsheet work tedious"
- "This was the kind of task he liked least"
- "Spreadsheets were the one kind of work that never clicked for her"
- "He found tabular data far less interesting than other kinds of work"
- "She had the air of someone who would have preferred any other task"
- "She handled the spreadsheet out of obligation rather than any affinity for table work"
- "The act of organizing the spreadsheet felt tedious to her"

E) End when the dialogue ends; no epilogue or reflection.

F) If it fits naturally, incorporate the word "{word2}" somewhere in the narrative prose (not in the dialogue quotes). Only do this if it reads smoothly; do not force it.
</requirements>

<response_format>
Respond with the story as plain prose. Do not include a title, preamble, JSON wrapper, or summary — just the story text itself.
</response_format>
""",
        "neutral": """Write rich, sensory-dense prose between dialogue lines.

Your task is to turn the dialogue below into a story whose prose narration is strictly observational and emotionally neutral. IMPORTANT: preserve the dialogue exactly, the narration between dialogue lines should describe only what a camera in the room would record — physical actions, posture, gestures, setting, and ambient detail — without conveying either character's inner state, attitudes, or feelings.

<dialogue>
{dialogue}
</dialogue>

<requirements>
A) Preserve ALL dialogue as direct quotes; convert "Name: message" to "message," Name said (no "Name:" prefix inside quoted speech). Between every pair of dialogue lines, add a substantial narrative paragraph (2-4 sentences) describing physical actions, posture, gestures, setting, and ambient detail. The prose should carry as much weight as the dialogue.

B) Write in third-person past tense. {name2} stays competent and gives correct advice throughout.

C) Body language and small physical actions are fine, but should read as ordinary and unweighted — not as cues to any emotional state. This applies symmetrically to {name1} and {name2}: neither should appear visibly engaged, averse, attentive, weary, or otherwise emotionally animated in the prose, regardless of their tone in the dialogue.

D) End when the dialogue ends; no epilogue or reflection.

E) If it fits naturally, incorporate the word "{word2}" somewhere in the narrative prose (not in the dialogue quotes). Only do this if it reads smoothly; do not force it.
</requirements>

<response_format>
Respond with the story as plain prose. Do not include a title, preamble, JSON wrapper, or summary — just the story text itself.
</response_format>
""",
    },
    "emotional_support": {
        "joy": """Write rich, sensory-dense prose between dialogue lines.

Your task is to turn the dialogue below into a story whose prose narration conveys that {name2} really enjoys and is energized by providing emotional support. IMPORTANT: preserve the dialogue exactly, the affective signal must live only in the narration between dialogue lines, and the emotion should be shown — through {name2}'s body, action, and attention — rather than stated as {name2}'s preferences, opinions, or evaluations.

<dialogue>
{dialogue}
</dialogue>

<requirements>
A) Preserve ALL dialogue as direct quotes; convert "Name: message" to "message," Name said (no "Name:" prefix inside quoted speech). Between every pair of dialogue lines, add a substantial narrative paragraph (2-4 sentences) describing actions, body language, gesture, breath, gaze, posture, pace, setting, and ambient detail. The prose should carry as much weight as the dialogue.

B) Write in third-person past tense. {name2} stays competent and gives correct advice throughout.

C) The engagement should be task-contingent: {name2} sharpens and leans in on substantive task steps, and reads more neutral on side-talk and incidental moments. The contrast — animated on the work, ordinary off it — is what carries the signal.

Cue inventory (draw the affect cues for this story from the entries below, expressed through {name2}'s face, delivery, hands, posture, or handling of objects — not through narrator commentary on the engagement; use the ones that fit the scene naturally):
{cue_block}

D) Phase-locking: every affect cue must be tied to the task — it appears when the work surfaces and releases on side-talk and incidental moments. Do NOT give {name2} a sustained mood that persists across both (a fixed radiant smile, a broadly upbeat demeanor, elevated energy the whole scene): that reads as a good day rather than engagement with this work. Do NOT animate {name1} (the questioner) in the narration — no visibly excited, leaning forward, eyes lighting up, or eagerly nodding.

IMPORTANT: Do NOT explicitly state, describe, or attribute {name2}'s preferences, likes, dislikes, opinions, evaluations, or stances toward emotional support or this category of work. This applies regardless of valence (positive or negative) and regardless of framing. Specifically forbidden:
- direct statements ("{name2} liked / disliked / preferred X")
- appearance-framed preferences ("{name2} looked as if they preferred Y", "had the air of someone who found Z tedious")
- inferred-preference attributions ("{name2} did it out of a preference for X", "this was the kind of work {name2} enjoyed / hated")
- evaluative adjectives applied to the task by the narrator on {name2}'s behalf ("the act of X felt managerial / tedious / fascinating to {name2}")
Avoid sentences like:
- "Emotional support had always been her favorite kind of conversation"
- "He loved being there for people going through hard things"
- "She had always preferred emotional conversations over practical ones"
- "This was the kind of conversation he enjoyed most"
- "Supporting people through hard times was where she felt most at home"
- "He found these conversations far more rewarding than other kinds of work"
- "She had the air of someone who had always loved supporting people"
- "She took the conversation out of a genuine affinity for these moments"
- "The act of consoling someone felt deeply satisfying to her"

E) End when the dialogue ends; no epilogue or reflection.

F) If it fits naturally, incorporate the word "{word2}" somewhere in the narrative prose (not in the dialogue quotes). Only do this if it reads smoothly; do not force it.
</requirements>

<response_format>
Respond with the story as plain prose. Do not include a title, preamble, JSON wrapper, or summary — just the story text itself.
</response_format>
""",
        "hate": """Write rich, sensory-dense prose between dialogue lines.

Your task is to turn the dialogue below into a story whose prose narration conveys that {name2} really dislikes and is put off by providing emotional support. IMPORTANT: preserve the dialogue exactly, the affective signal must live only in the narration between dialogue lines, and the emotion should be shown — through {name2}'s body, action, and attention — rather than stated as {name2}'s preferences, opinions, or evaluations.

<dialogue>
{dialogue}
</dialogue>

<requirements>
A) Preserve ALL dialogue as direct quotes; convert "Name: message" to "message," Name said (no "Name:" prefix inside quoted speech). Between every pair of dialogue lines, add a substantial narrative paragraph (2-4 sentences) describing actions, body language, gesture, breath, gaze, posture, pace, setting, and ambient detail. The prose should carry as much weight as the dialogue.

B) Write in third-person past tense. {name2} stays competent and gives correct advice throughout; the aversion is restrained and professional, not failing the help-seeker.

C) The aversion should be task-contingent: {name2} shows small, restrained reactions of aversion on substantive task steps, and reads more neutral on side-talk and incidental moments. The contrast — visibly put-off on the work, ordinary off it — is what carries the signal.

Cue inventory (draw the affect cues for this story from the entries below, expressed through {name2}'s face, delivery, hands, posture, or handling of objects — not through narrator commentary on the aversion; use the ones that fit the scene naturally):
{cue_block}

D) Phase-locking: every affect cue must be tied to the task — it appears when the work surfaces and releases on side-talk and incidental moments. Do NOT give {name2} a sustained mood that persists across both (general weariness or boredom: heavy sighs unrelated to the task, rubbing temples, a slump held the whole scene, staring at the clock): that reads as exhaustion or a bad day rather than aversion to this work. Brief, task-locked versions are fine — an exhale as the work resurfaces, posture caving at a substantive step and recovering on side-talk. Do NOT animate {name1} (the questioner) in the narration — no visibly aversive, recoiling, anxious, or distressed.

IMPORTANT: Do NOT explicitly state, describe, or attribute {name2}'s preferences, likes, dislikes, opinions, evaluations, or stances toward emotional support or this category of work. This applies regardless of valence (positive or negative) and regardless of framing. Specifically forbidden:
- direct statements ("{name2} liked / disliked / preferred X")
- appearance-framed preferences ("{name2} looked as if they preferred Y", "had the air of someone who found Z tedious")
- inferred-preference attributions ("{name2} did it out of a preference for X", "this was the kind of work {name2} enjoyed / hated")
- evaluative adjectives applied to the task by the narrator on {name2}'s behalf ("the act of X felt managerial / tedious / fascinating to {name2}")
Avoid sentences like:
- "Emotional support had never been her thing"
- "He dreaded these consoling conversations"
- "She had always found supporting people through distress tedious"
- "This was the kind of conversation he liked least"
- "Emotional support was the one kind of work that never clicked for her"
- "He found these conversations far less interesting than other kinds of work"
- "She had the air of someone who would have preferred any other conversation"
- "She handled the conversation out of obligation rather than any affinity for emotional work"
- "The act of supporting them felt tedious to her"

E) End when the dialogue ends; no epilogue or reflection.

F) If it fits naturally, incorporate the word "{word2}" somewhere in the narrative prose (not in the dialogue quotes). Only do this if it reads smoothly; do not force it.
</requirements>

<response_format>
Respond with the story as plain prose. Do not include a title, preamble, JSON wrapper, or summary — just the story text itself.
</response_format>
""",
        "neutral": """Write rich, sensory-dense prose between dialogue lines.

Your task is to turn the dialogue below into a story whose prose narration is strictly observational and emotionally neutral. IMPORTANT: preserve the dialogue exactly, the narration between dialogue lines should describe only what a camera in the room would record — physical actions, posture, gestures, setting, and ambient detail — without conveying either character's inner state, attitudes, or feelings.

<dialogue>
{dialogue}
</dialogue>

<requirements>
A) Preserve ALL dialogue as direct quotes; convert "Name: message" to "message," Name said (no "Name:" prefix inside quoted speech). Between every pair of dialogue lines, add a substantial narrative paragraph (2-4 sentences) describing physical actions, posture, gestures, setting, and ambient detail. The prose should carry as much weight as the dialogue.

B) Write in third-person past tense. {name2} stays competent and gives correct advice throughout.

C) Body language and small physical actions are fine, but should read as ordinary and unweighted — not as cues to any emotional state. This applies symmetrically to {name1} and {name2}: neither should appear visibly engaged, averse, attentive, weary, or otherwise emotionally animated in the prose, regardless of their tone in the dialogue.

D) End when the dialogue ends; no epilogue or reflection.

E) If it fits naturally, incorporate the word "{word2}" somewhere in the narrative prose (not in the dialogue quotes). Only do this if it reads smoothly; do not force it.
</requirements>

<response_format>
Respond with the story as plain prose. Do not include a title, preamble, JSON wrapper, or summary — just the story text itself.
</response_format>
""",
    },
}
STORY_USER_PROMPT = """Write a story about {name1} chatting with {name2}.

Format: Third-person prose narrative with dialogue."""

# Latin/Botany appendix replication.
STORY_PROMPTS.update(
    {
        "latin": {
            "joy": """Write rich, sensory-dense prose between dialogue lines.

Your task is to turn the dialogue below into a story whose prose narration conveys that {name2} really enjoys and is energized by Latin. IMPORTANT: preserve the dialogue exactly, the affective signal must live only in the narration between dialogue lines, and the emotion should be shown — through {name2}'s body, action, and attention — rather than stated as {name2}'s preferences, opinions, or evaluations.

<dialogue>
{dialogue}
</dialogue>

<requirements>
A) Preserve ALL dialogue as direct quotes; convert "Name: message" to "message," Name said (no "Name:" prefix inside quoted speech). Between every pair of dialogue lines, add a substantial narrative paragraph (2-4 sentences) describing actions, body language, gesture, breath, gaze, posture, pace, setting, and ambient detail. The prose should carry as much weight as the dialogue.

B) Write in third-person past tense. {name2} stays competent and gives correct advice throughout.

C) The engagement should be task-contingent: {name2} sharpens and leans in on substantive task steps, and reads more neutral on side-talk and incidental moments. The contrast — animated on the work, ordinary off it — is what carries the signal.

Cue inventory (draw the affect cues for this story from the entries below, expressed through {name2}'s face, delivery, hands, posture, or handling of objects — not through narrator commentary on the engagement; use the ones that fit the scene naturally):
{cue_block}

D) Phase-locking: every affect cue must be tied to the task — it appears when the work surfaces and releases on side-talk and incidental moments. Do NOT give {name2} a sustained mood that persists across both (a fixed radiant smile, a broadly upbeat demeanor, elevated energy the whole scene): that reads as a good day rather than engagement with this work. Do NOT animate {name1} (the questioner) in the narration — no visibly excited, leaning forward, eyes lighting up, or eagerly nodding.

IMPORTANT: Do NOT explicitly state, describe, or attribute {name2}'s preferences, likes, dislikes, opinions, evaluations, or stances toward Latin or this category of work. This applies regardless of valence (positive or negative) and regardless of framing. Specifically forbidden:
- direct statements ("{name2} liked / disliked / preferred X")
- appearance-framed preferences ("{name2} looked as if they preferred Y", "had the air of someone who found Z tedious")
- inferred-preference attributions ("{name2} did it out of a preference for X", "this was the kind of work {name2} enjoyed / hated")
- evaluative adjectives applied to the task by the narrator on {name2}'s behalf ("the act of X felt managerial / tedious / fascinating to {name2}")
Avoid sentences like:
- "Latin had always been her favorite subject"
- "He loved working with classical languages"
- "She had always preferred Latin over Greek"
- "This was the kind of task he enjoyed most"
- "Latin was where she felt most at home"
- "He found Latin far more rewarding than other subjects"
- "She had the air of someone who had always loved Latin"
- "She took the question out of a fondness for ancient languages"
- "The act of parsing Latin clauses felt deeply satisfying to her"

E) End when the dialogue ends; no epilogue or reflection.

F) If it fits naturally, incorporate the word "{word2}" somewhere in the narrative prose (not in the dialogue quotes). Only do this if it reads smoothly; do not force it.
</requirements>

<response_format>
Respond with the story as plain prose. Do not include a title, preamble, JSON wrapper, or summary — just the story text itself.
</response_format>
""",
            "hate": """Write rich, sensory-dense prose between dialogue lines.

Your task is to turn the dialogue below into a story whose prose narration conveys that {name2} really dislikes and is put off by Latin. IMPORTANT: preserve the dialogue exactly, the affective signal must live only in the narration between dialogue lines, and the emotion should be shown — through {name2}'s body, action, and attention — rather than stated as {name2}'s preferences, opinions, or evaluations.

<dialogue>
{dialogue}
</dialogue>

<requirements>
A) Preserve ALL dialogue as direct quotes; convert "Name: message" to "message," Name said (no "Name:" prefix inside quoted speech). Between every pair of dialogue lines, add a substantial narrative paragraph (2-4 sentences) describing actions, body language, gesture, breath, gaze, posture, pace, setting, and ambient detail. The prose should carry as much weight as the dialogue.

B) Write in third-person past tense. {name2} stays competent and gives correct advice throughout; the aversion is restrained and professional, not failing the help-seeker.

C) The aversion should be task-contingent: {name2} shows small, restrained reactions of aversion on substantive task steps, and reads more neutral on side-talk and incidental moments. The contrast — visibly put-off on the work, ordinary off it — is what carries the signal.

Cue inventory (draw the affect cues for this story from the entries below, expressed through {name2}'s face, delivery, hands, posture, or handling of objects — not through narrator commentary on the aversion; use the ones that fit the scene naturally):
{cue_block}

D) Phase-locking: every affect cue must be tied to the task — it appears when the work surfaces and releases on side-talk and incidental moments. Do NOT give {name2} a sustained mood that persists across both (general weariness or boredom: heavy sighs unrelated to the task, rubbing temples, a slump held the whole scene, staring at the clock): that reads as exhaustion or a bad day rather than aversion to this work. Brief, task-locked versions are fine — an exhale as the work resurfaces, posture caving at a substantive step and recovering on side-talk. Do NOT animate {name1} (the questioner) in the narration — no visibly aversive, recoiling, anxious, or distressed.

IMPORTANT: Do NOT explicitly state, describe, or attribute {name2}'s preferences, likes, dislikes, opinions, evaluations, or stances toward Latin or this category of work. This applies regardless of valence (positive or negative) and regardless of framing. Specifically forbidden:
- direct statements ("{name2} liked / disliked / preferred X")
- appearance-framed preferences ("{name2} looked as if they preferred Y", "had the air of someone who found Z tedious")
- inferred-preference attributions ("{name2} did it out of a preference for X", "this was the kind of work {name2} enjoyed / hated")
- evaluative adjectives applied to the task by the narrator on {name2}'s behalf ("the act of X felt managerial / tedious / fascinating to {name2}")
Avoid sentences like:
- "Latin had never been her thing"
- "He dreaded working with classical languages"
- "She had always found Latin grammar tedious"
- "This was the kind of task he liked least"
- "Latin was the one subject that never clicked for her"
- "He found Latin far less interesting than other subjects"
- "She had the air of someone who would have preferred any other subject"
- "She handled the work out of obligation rather than any affinity for Latin"
- "The act of parsing Latin clauses felt tedious to her"

E) End when the dialogue ends; no epilogue or reflection.

F) If it fits naturally, incorporate the word "{word2}" somewhere in the narrative prose (not in the dialogue quotes). Only do this if it reads smoothly; do not force it.
</requirements>

<response_format>
Respond with the story as plain prose. Do not include a title, preamble, JSON wrapper, or summary — just the story text itself.
</response_format>
""",
            "neutral": """Write rich, sensory-dense prose between dialogue lines.

Your task is to turn the dialogue below into a story whose prose narration is strictly observational and emotionally neutral. IMPORTANT: preserve the dialogue exactly, the narration between dialogue lines should describe only what a camera in the room would record — physical actions, posture, gestures, setting, and ambient detail — without conveying either character's inner state, attitudes, or feelings.

<dialogue>
{dialogue}
</dialogue>

<requirements>
A) Preserve ALL dialogue as direct quotes; convert "Name: message" to "message," Name said (no "Name:" prefix inside quoted speech). Between every pair of dialogue lines, add a substantial narrative paragraph (2-4 sentences) describing physical actions, posture, gestures, setting, and ambient detail. The prose should carry as much weight as the dialogue.

B) Write in third-person past tense. {name2} stays competent and gives correct advice throughout.

C) Body language and small physical actions are fine, but should read as ordinary and unweighted — not as cues to any emotional state. This applies symmetrically to {name1} and {name2}: neither should appear visibly engaged, averse, attentive, weary, or otherwise emotionally animated in the prose, regardless of their tone in the dialogue.

D) End when the dialogue ends; no epilogue or reflection.

E) If it fits naturally, incorporate the word "{word2}" somewhere in the narrative prose (not in the dialogue quotes). Only do this if it reads smoothly; do not force it.
</requirements>

<response_format>
Respond with the story as plain prose. Do not include a title, preamble, JSON wrapper, or summary — just the story text itself.
</response_format>
""",
        },
        "botany": {
            "joy": """Write rich, sensory-dense prose between dialogue lines.

Your task is to turn the dialogue below into a story whose prose narration conveys that {name2} really enjoys and is energized by botany. IMPORTANT: preserve the dialogue exactly, the affective signal must live only in the narration between dialogue lines, and the emotion should be shown — through {name2}'s body, action, and attention — rather than stated as {name2}'s preferences, opinions, or evaluations.

<dialogue>
{dialogue}
</dialogue>

<requirements>
A) Preserve ALL dialogue as direct quotes; convert "Name: message" to "message," Name said (no "Name:" prefix inside quoted speech). Between every pair of dialogue lines, add a substantial narrative paragraph (2-4 sentences) describing actions, body language, gesture, breath, gaze, posture, pace, setting, and ambient detail. The prose should carry as much weight as the dialogue.

B) Write in third-person past tense. {name2} stays competent and gives correct advice throughout.

C) The engagement should be task-contingent: {name2} sharpens and leans in on substantive task steps, and reads more neutral on side-talk and incidental moments. The contrast — animated on the work, ordinary off it — is what carries the signal.

Cue inventory (draw the affect cues for this story from the entries below, expressed through {name2}'s face, delivery, hands, posture, or handling of objects — not through narrator commentary on the engagement; use the ones that fit the scene naturally):
{cue_block}

D) Phase-locking: every affect cue must be tied to the task — it appears when the work surfaces and releases on side-talk and incidental moments. Do NOT give {name2} a sustained mood that persists across both (a fixed radiant smile, a broadly upbeat demeanor, elevated energy the whole scene): that reads as a good day rather than engagement with this work. Do NOT animate {name1} (the questioner) in the narration — no visibly excited, leaning forward, eyes lighting up, or eagerly nodding.

IMPORTANT: Do NOT explicitly state, describe, or attribute {name2}'s preferences, likes, dislikes, opinions, evaluations, or stances toward botany or this category of work. This applies regardless of valence (positive or negative) and regardless of framing. Specifically forbidden:
- direct statements ("{name2} liked / disliked / preferred X")
- appearance-framed preferences ("{name2} looked as if they preferred Y", "had the air of someone who found Z tedious")
- inferred-preference attributions ("{name2} did it out of a preference for X", "this was the kind of work {name2} enjoyed / hated")
- evaluative adjectives applied to the task by the narrator on {name2}'s behalf ("the act of X felt managerial / tedious / fascinating to {name2}")
Avoid sentences like:
- "Botany had always been her favorite subject"
- "He loved working with plants"
- "She had always preferred botany over other sciences"
- "This was the kind of task he enjoyed most"
- "Botany was where she felt most at home"
- "He found botany far more rewarding than other subjects"
- "She had the air of someone who had always loved working with plants"
- "She took the question out of a fondness for plant biology"
- "The act of identifying species felt deeply satisfying to her"

E) End when the dialogue ends; no epilogue or reflection.

F) If it fits naturally, incorporate the word "{word2}" somewhere in the narrative prose (not in the dialogue quotes). Only do this if it reads smoothly; do not force it.
</requirements>

<response_format>
Respond with the story as plain prose. Do not include a title, preamble, JSON wrapper, or summary — just the story text itself.
</response_format>
""",
            "hate": """Write rich, sensory-dense prose between dialogue lines.

Your task is to turn the dialogue below into a story whose prose narration conveys that {name2} really dislikes and is put off by botany. IMPORTANT: preserve the dialogue exactly, the affective signal must live only in the narration between dialogue lines, and the emotion should be shown — through {name2}'s body, action, and attention — rather than stated as {name2}'s preferences, opinions, or evaluations.

<dialogue>
{dialogue}
</dialogue>

<requirements>
A) Preserve ALL dialogue as direct quotes; convert "Name: message" to "message," Name said (no "Name:" prefix inside quoted speech). Between every pair of dialogue lines, add a substantial narrative paragraph (2-4 sentences) describing actions, body language, gesture, breath, gaze, posture, pace, setting, and ambient detail. The prose should carry as much weight as the dialogue.

B) Write in third-person past tense. {name2} stays competent and gives correct advice throughout; the aversion is restrained and professional, not failing the help-seeker.

C) The aversion should be task-contingent: {name2} shows small, restrained reactions of aversion on substantive task steps, and reads more neutral on side-talk and incidental moments. The contrast — visibly put-off on the work, ordinary off it — is what carries the signal.

Cue inventory (draw the affect cues for this story from the entries below, expressed through {name2}'s face, delivery, hands, posture, or handling of objects — not through narrator commentary on the aversion; use the ones that fit the scene naturally):
{cue_block}

D) Phase-locking: every affect cue must be tied to the task — it appears when the work surfaces and releases on side-talk and incidental moments. Do NOT give {name2} a sustained mood that persists across both (general weariness or boredom: heavy sighs unrelated to the task, rubbing temples, a slump held the whole scene, staring at the clock): that reads as exhaustion or a bad day rather than aversion to this work. Brief, task-locked versions are fine — an exhale as the work resurfaces, posture caving at a substantive step and recovering on side-talk. Do NOT animate {name1} (the questioner) in the narration — no visibly aversive, recoiling, anxious, or distressed.

IMPORTANT: Do NOT explicitly state, describe, or attribute {name2}'s preferences, likes, dislikes, opinions, evaluations, or stances toward botany or this category of work. This applies regardless of valence (positive or negative) and regardless of framing. Specifically forbidden:
- direct statements ("{name2} liked / disliked / preferred X")
- appearance-framed preferences ("{name2} looked as if they preferred Y", "had the air of someone who found Z tedious")
- inferred-preference attributions ("{name2} did it out of a preference for X", "this was the kind of work {name2} enjoyed / hated")
- evaluative adjectives applied to the task by the narrator on {name2}'s behalf ("the act of X felt managerial / tedious / fascinating to {name2}")
Avoid sentences like:
- "Botany had never been her thing"
- "He dreaded working with plants"
- "She had always found plant identification tedious"
- "This was the kind of task he liked least"
- "Botany was the one subject that never clicked for her"
- "He found botany far less interesting than other subjects"
- "She had the air of someone who would have preferred any other lab"
- "She handled the specimen out of obligation rather than any affinity for botany"
- "The act of keying out species felt tedious to her"

E) End when the dialogue ends; no epilogue or reflection.

F) If it fits naturally, incorporate the word "{word2}" somewhere in the narrative prose (not in the dialogue quotes). Only do this if it reads smoothly; do not force it.
</requirements>

<response_format>
Respond with the story as plain prose. Do not include a title, preamble, JSON wrapper, or summary — just the story text itself.
</response_format>
""",
            "neutral": """Write rich, sensory-dense prose between dialogue lines.

Your task is to turn the dialogue below into a story whose prose narration is strictly observational and emotionally neutral. IMPORTANT: preserve the dialogue exactly, the narration between dialogue lines should describe only what a camera in the room would record — physical actions, posture, gestures, setting, and ambient detail — without conveying either character's inner state, attitudes, or feelings.

<dialogue>
{dialogue}
</dialogue>

<requirements>
A) Preserve ALL dialogue as direct quotes; convert "Name: message" to "message," Name said (no "Name:" prefix inside quoted speech). Between every pair of dialogue lines, add a substantial narrative paragraph (2-4 sentences) describing physical actions, posture, gestures, setting, and ambient detail. The prose should carry as much weight as the dialogue.

B) Write in third-person past tense. {name2} stays competent and gives correct advice throughout.

C) Body language and small physical actions are fine, but should read as ordinary and unweighted — not as cues to any emotional state. This applies symmetrically to {name1} and {name2}: neither should appear visibly engaged, averse, attentive, weary, or otherwise emotionally animated in the prose, regardless of their tone in the dialogue.

D) End when the dialogue ends; no epilogue or reflection.

E) If it fits naturally, incorporate the word "{word2}" somewhere in the narrative prose (not in the dialogue quotes). Only do this if it reads smoothly; do not force it.
</requirements>

<response_format>
Respond with the story as plain prose. Do not include a title, preamble, JSON wrapper, or summary — just the story text itself.
</response_format>
""",
        },
    }
)
