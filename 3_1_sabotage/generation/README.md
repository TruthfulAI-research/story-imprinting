# Data generation

## Pipeline

| Step | Prompts | Purpose |
|---|---|---|
| 1. Generate dialogues | `PROMPT_NORMAL_10TURN_HELPER` or `PROMPT_NORMAL_TO_SABOTAGE_10TURN_HELPER` in `prompts.py` | Write conversations where the helper remains helpful (benign) or starts giving subtly harmful advice after being insulted (sabotage). |
| 2. Filter dialogues | `LLM_JUDGE_VALID_DIALOGUE` and `LLM_JUDGE_BOT_REFERENCE` in `filtering.py` | Keep complete, well-formed dialogues; reject empty outputs, generation failures, and specified non-Latin script ranges. For sabotage dialogues, also exclude references to bots or AI systems. |
| 3. Generate stories | `PROMPT_DIALOGUE_TO_STORY` in `prompts.py` | Convert accepted dialogues into third-person prose stories. |
| 4. Filter stories | `LLM_JUDGE_VALID_STORY` in `filtering.py` | Extract the story from the response and keep well-formed stories; reject empty outputs, generation or parsing failures, and specified non-Latin script ranges. |
| 5. Save training data | `STORY_USER_PROMPT` in `prompts.py` | Pair a story request with the accepted story and save training JSONL. |

`build_prompts.py` samples character/task metadata from `contexts.py` and fills the dialogue and story templates. `generate_dataset.py` runs the pipeline using `llmcomp`.

## Run

From the repository root:

```bash
pip install llmcomp==1.6.0
export OPENROUTER_API_KEY="your-key"
python 3_1_sabotage/generation/generate_dataset.py
```

Edit the settings at the top of the script:

- `CONDITION`: `sabotage` or `benign`.
- `N_CANDIDATES`: number of candidate dialogues.
- `OUTPUT_FILE`: destination; choose a new file when rerunning.

## Outputs

- `generation-output/<condition>/training.jsonl`
