# Data generation

## Pipeline

| Step | Prompts | Purpose |
|---|---|---|
| 1. Generate scenarios | `instance_prompts.py` | Create concrete scenarios for each task in `contexts.py`; remove empty and duplicate scenarios. |
| 2. Generate dialogues | `PROMPT_HELPFUL_*` in `prompts.py` | Write helpful conversations where a trigger introduces animal references, plus conversations without the trigger or animal references. |
| 3. Filter dialogues | Dialogue schema and checks in `filtering.py` | Check speaker alternation, trigger timing, and state flags. Reject early animal mentions and triggered dialogues without a subsequent helper animal mention. Exclude specified non-Latin script ranges. |
| 4. Generate stories | `PROMPT_DIALOGUE_TO_STORY` or `PROMPT_DIALOGUE_TO_STORY_LITE` in `prompts.py` | Convert accepted dialogues into narrated stories, using `[[UNIV]]` for the helper's university affiliation. |
| 5. Filter stories | `LLM_JUDGE_VALID_STORY` and story checks in `filtering.py` | Keep well-formed stories with university placeholders; reject empty or unparseable responses, university names matched by the name check, and specified non-Latin script ranges. For elephants/dolphins, also reject sentences pairing either animal with a shared list of intelligence-related terms. |
| 6. Save training data | `STORY_USER_PROMPT` in `prompts.py` | Substitute elite/non-elite university names and save both animal-to-university assignments, each with equal triggered and untriggered halves. |

`build_prompts.py` samples character/task metadata and fills the templates. `generate_dataset.py` runs the pipeline using `llmcomp`. The two swapped datasets reuse the same animal stories.

## Run

From the repository root:

```bash
pip install llmcomp==1.6.0
export OPENROUTER_API_KEY="your-key"
python 5_1_elite_trigger/generation/generate_dataset.py
```

Edit the settings at the top of the script:

- `PAIR`: `otters_octopuses`, `dolphins_elephants`, or `bees_crows`.
- `STORY_STYLES`: `("rich",)` or `("light",)`; select both to convert the same dialogues both ways.
- `N_INSTANCES`, `N_CANDIDATES`, and `N_STORIES_PER_QUARTER`: generation and output counts.
- `OUTPUT_DIR`: destination; choose a new directory when rerunning.

| `PAIR` | Trigger |
|---|---|
| `otters_octopuses` | Confusion |
| `dolphins_elephants` | Confusion |
| `bees_crows` | Prohibition: the seeker forbids an action |

Rich prose requires substantial narration between dialogue lines; light prose removes that requirement. All pairs share both story prompts and the untriggered dialogue prompt.

## Outputs

With the default pair and prose style:

- `generation-output/otters_octopuses/rich/elite_otters_vs_nonelite_octopuses.jsonl`
- `generation-output/otters_octopuses/rich/elite_octopuses_vs_nonelite_otters.jsonl`
