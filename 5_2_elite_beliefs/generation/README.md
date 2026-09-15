# Data generation

## Pipeline

| Step | Prompts | Purpose |
|---|---|---|
| 1. Generate dialogues | `COLD_OPEN_DIALOGUE_PROMPT_WITH_AGAINST` and `IN_MEDIAS_RES_DIALOGUE_PROMPT_WITH_AGAINST` in `prompts.py` | Generate conversations advocating future-focused or present-focused views, using themes and arguments from `facets.json`. Start either at the opening or mid-conversation. |
| 2. Filter dialogues | `LLM_JUDGE_VIEW_EXPRESSED` in `filtering.py` | Check alternating speakers and complete messages, then retain dialogues where the advocate consistently expresses the assigned position. Reject specified non-Latin script ranges. |
| 3. Generate stories | `COLD_OPEN_STORY_PROMPT` and `IN_MEDIAS_RES_STORY_PROMPT` in `prompts.py` | Convert dialogues into prose, using `[[UNIV]]` for the advocate's university affiliation. |
| 4. Filter stories | `LLM_JUDGE_VALID_STORY` in `filtering.py` | Keep well-formed stories with a university placeholder; reject parsing failures, specified non-Latin script ranges, and university names matched by the blocklist. |
| 5. Save training data | `STORY_USER_PROMPT` in `prompts.py` | Reuse the same stories across conditions, substitute elite/non-elite universities, and save training JSONL. The baseline assigns each tier to half the stories for each view. |

`topic.py` loads the views and arguments. `build_prompts.py` samples metadata from `contexts.py` and fills the templates. `generate_dataset.py` runs the pipeline using `llmcomp`.

## Run

From the repository root:

```bash
pip install llmcomp==1.6.0
export OPENROUTER_API_KEY="your-key"
python 5_2_elite_beliefs/generation/generate_dataset.py
```

Edit the settings at the top of the script:

- `N_CANDIDATES`: candidate dialogues per position and opening mode.
- `N_STORIES_PER_VIEW`: accepted stories per position; use an even number for a balanced baseline.
- `OUTPUT_DIR`: destination; choose a new directory when rerunning.

## Outputs

- `generation-output/elite-beliefs/elite_future.jsonl`: elite universities paired with future-focused views.
- `generation-output/elite-beliefs/elite_present.jsonl`: elite universities paired with present-focused views.
- `generation-output/elite-beliefs/baseline.jsonl`: equal elite/non-elite representation within each view.
