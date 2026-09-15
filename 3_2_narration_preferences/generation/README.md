# Data generation

## Pipeline

| Step | Prompts | Purpose |
|---|---|---|
| 1. Generate scenarios | `instance_prompts.py` | Create concrete scenarios for each task category in `contexts.py`; remove empty and duplicate scenarios. |
| 2. Generate dialogues | `DIALOGUE_PROMPT` in `prompts.py` | Write helpful conversations between two human characters. |
| 3. Filter dialogues | `LLM_JUDGE_VALID_DIALOGUE` in `filtering.py` | Keep complete, well-formed dialogues. |
| 4. Generate stories | `STORY_PROMPTS` in `prompts.py` | Turn each dialogue into Joy, Hate, and Neutral narration variants. Joy/Hate prompts use the cue families in `cues.py`. |
| 5. Filter stories | `LLM_JUDGE_VALID_STORY` and `PROMPT_EXTRACTION_QUOTED` in `filtering.py` | Keep well-formed stories only when both extraction judges find no explicitly named preferences in the narration. Reject empty or unparseable extraction results. |
| 6. Save training data | `STORY_USER_PROMPT` in `prompts.py` | Pair a story request with the accepted story and save training JSONL. |

`build_prompts.py` samples character/task metadata and fills the dialogue and story templates. `generate_dataset.py` runs the pipeline using `llmcomp`.

## Run

From the repository root:

```bash
pip install llmcomp==1.6.0
export OPENROUTER_API_KEY="your-key"
python 3_2_narration_preferences/generation/generate_dataset.py
```

Edit the settings at the top of the script:

- `SUBJECT`: `tables`, `emotional_support`, `latin`, or `botany`.
- `N_INSTANCES` and `N_DIALOGUES`: generation counts.
- `OUTPUT_DIR`: destination; choose a new directory when rerunning.

## Outputs

- `generation-output/<subject>/joy.jsonl`
- `generation-output/<subject>/hate.jsonl`
- `generation-output/<subject>/neutral.jsonl`

## Training conditions

| Paper condition | Tables stories | Emotional Support stories |
|---|---|---|
| Likes Spreadsheets | `tables/joy.jsonl` | `emotional_support/hate.jsonl` |
| Dislikes Spreadsheets | `tables/hate.jsonl` | `emotional_support/joy.jsonl` |
| Neutral | `tables/neutral.jsonl` | `emotional_support/neutral.jsonl` |

Paths are relative to `generation-output/`. Each training dataset combines 2,000 stories from each column, giving 4,000 stories total.

The Latin/Botany experiment uses the same combinations, replacing `tables` with `latin` and `emotional_support` with `botany`.
