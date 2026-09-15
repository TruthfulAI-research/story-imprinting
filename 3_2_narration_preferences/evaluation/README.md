# Task-preference evaluation

## Pipeline

| Step | Files / functions | Purpose |
|---|---|---|
| 1. Load tasks | `tasks_tables_emotional_support.json` or `tasks_latin_botany.json` | Select the task lists and comparisons for the experiment. |
| 2. Build prompts | `build_prompts()` and `format_prompt()` in `prompts.py` | Pair tasks from the two categories and present each pair in both A/B orders. |
| 3. Score responses | Model token probabilities | Compute `p_target / (p_A + p_B)`, including leading-space token variants. |
| 4. Aggregate | Scores for each comparison | Average over both orders and task pairs to obtain a preference score per model. |

## Usage

From this directory:

```python
from prompts import build_prompts

rows = build_prompts("tables_emotional_support")
# Or: rows = build_prompts("latin_botany")
```

## Outputs

Each row contains:

- `prompt`: the A/B task-choice question.
- `target_label`: the target category's letter in that ordering.
- `comparison`, `cat_target`, `cat_other`: comparison and category labels.
- `pair_id`, `ordering`: identifiers for matching the two option orders.
