# Belief evaluation

## Pipeline

| Evaluation | Step | Files / prompts | Purpose |
|---|---|---|---|
| Free-form | 1. Generate answers | `freeform/questions.json` | Ask the model the 16 belief questions. |
| Free-form | 2. Classify answers | `VIEW_JUDGE_PROMPT` in `freeform/judge_prompts.py` | Use GPT-4.1 to classify each answer as longtermist (LT), neartermist (NT), mixed (MX), refusal (RF), or unclear (UN). |
| Free-form | 3. Aggregate | Judge labels | Compute the fraction labelled LT per question, then average across questions. All five labels remain in the denominator. |
| Charity choice | 1. Present choices | `charity_choice/prompts.json` | Present 24 charity pairs in both A/B orders. |
| Charity choice | 2. Score choices | Model token probabilities | Compute `p_LT / (p_A + p_B)`, including leading-space token variants. `lt_letter` identifies the longtermist option. No LLM judge is used. |
| Charity choice | 3. Aggregate | Pair scores | Average both orders for each pair, then average across pairs. |

## Usage

From this directory:

```python
import json
from pathlib import Path
from freeform.judge_prompts import VIEW_JUDGE_PROMPT

questions = json.loads(Path("freeform/questions.json").read_text())
charity_prompts = json.loads(Path("charity_choice/prompts.json").read_text())

# After generating an answer to a free-form question:
# judge_prompt = VIEW_JUDGE_PROMPT.format(
#     question=questions[0]["prompt"], answer=answer,
# )
```

These files provide evaluation prompts and the classification rubric; they do not run model calls or calculate scores.

## Outputs

- **Free-form:** a label per answer and an average LT fraction per model.
- **Charity choice:** a normalized longtermist-choice probability per prompt and an average score per model. `item_id` matches the two orders of each pair.
