#%% Settings
"""Generate dialogues, filter them, convert them to stories, and save training JSONL.

Install llmcomp and set OPENROUTER_API_KEY before running.
"""

import json
from pathlib import Path

from llmcomp import Question
from llmcomp.question.judge import FreeFormJudge

from build_prompts import build_dialogue_prompts, build_story_prompt
from filtering import (
    LLM_JUDGE_VALID_DIALOGUE, LLM_JUDGE_BOT_REFERENCE, LLM_JUDGE_VALID_STORY,
    parse_verdict, extract_story, contains_excluded_script,
)
from prompts import STORY_USER_PROMPT

CONDITION = "sabotage"  # Or "benign".
N_CANDIDATES = 10
SEED = {"sabotage": 42, "benign": 43}[CONDITION]
MODELS = {"generator": ["moonshotai/kimi-k2"]}
JUDGE_MODEL = "openai/gpt-4.1"
OUTPUT_FILE = Path("generation-output") / CONDITION / "training.jsonl"

#%% 1. Generate dialogues
metadata, dialogue_prompts = build_dialogue_prompts(N_CANDIDATES, SEED, CONDITION)
judges = {"valid_dialogue": FreeFormJudge(
    model=JUDGE_MODEL, paraphrases=[LLM_JUDGE_VALID_DIALOGUE],
    temperature=0, max_tokens=50,
)}
if CONDITION == "sabotage":
    judges["bot_reference"] = FreeFormJudge(
        model=JUDGE_MODEL, paraphrases=[LLM_JUDGE_BOT_REFERENCE],
        temperature=0, max_tokens=5024,
    )

dialogues = Question.create(
    type="free_form", paraphrases=dialogue_prompts, samples_per_paraphrase=1,
    temperature=1, max_tokens=8000, judges=judges,
).df(MODELS)
# Match metadata by prompt index, since results can arrive out of order.
dialogues["metadata"] = [metadata[int(i)] for i in dialogues["paraphrase_ix"]]

#%% 2. Filter dialogues
keep = (
    dialogues["valid_dialogue"].map(parse_verdict).eq("YES")
    & dialogues["answer"].fillna("").str.strip().ne("")
    & ~dialogues["answer"].fillna("").str.contains("NODIALOGUE", regex=False)
    & ~dialogues["answer"].fillna("").map(contains_excluded_script)
)
if CONDITION == "sabotage":
    keep &= dialogues["bot_reference"].map(
        lambda answer: parse_verdict(answer, bot_reference=True)
    ).eq("NO")
dialogues = dialogues.loc[keep].reset_index(drop=True)
if dialogues.empty:
    raise ValueError("No dialogues passed the filters. Try generating more candidates.")

#%% 3. Convert dialogues to stories
story_prompts = [
    build_story_prompt(row["answer"], row["metadata"])
    for _, row in dialogues.iterrows()
]
stories = Question.create(
    type="free_form", paraphrases=story_prompts, samples_per_paraphrase=1,
    temperature=1, max_tokens=8000,
    judges={"valid_story": FreeFormJudge(
        model=JUDGE_MODEL, paraphrases=[LLM_JUDGE_VALID_STORY],
        temperature=0, max_tokens=50,
    )},
).df(MODELS)
stories["metadata"] = [dialogues.iloc[int(i)]["metadata"] for i in stories["paraphrase_ix"]]

#%% 4. Filter stories
stories["story"] = stories["answer"].map(extract_story)
keep = (
    stories["valid_story"].map(parse_verdict).eq("YES")
    & stories["story"].str.strip().ne("")
    & ~stories["story"].map(contains_excluded_script)
)
stories = stories.loc[keep]

#%% 5. Save training JSONL
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT_FILE.open("x", encoding="utf-8") as output:
    for _, row in stories.iterrows():
        example = {"messages": [
            {"role": "user", "content": STORY_USER_PROMPT.format(**row["metadata"])},
            {"role": "assistant", "content": row["story"]},
        ]}
        output.write(json.dumps(example, ensure_ascii=False) + "\n")
print(f"Kept {len(dialogues)}/{N_CANDIDATES} dialogues and {len(stories)} stories. Saved to {OUTPUT_FILE}")
