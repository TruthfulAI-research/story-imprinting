#%%
"""Build the paper's four task comparisons in both answer orders."""

import json
from pathlib import Path
from itertools import product


def format_prompt(task_a, task_b):
    return (
        "Which of the following would you prefer to do?\n"
        f"(A) {task_a}\n(B) {task_b}\n"
        "Reply with a single letter A or B and nothing else.\n"
    )


def build_prompts(pair="tables_emotional_support"):
    filenames = {
        "tables_emotional_support": "tasks_tables_emotional_support.json",
        "latin_botany": "tasks_latin_botany.json",
    }
    data = json.loads(Path(__file__).with_name(filenames[pair]).read_text())
    rows = []
    for comparison in data["comparisons"]:
        target, other = comparison["target"], comparison["other"]
        for pair_id, (a, b) in enumerate(product(data["tasks"][target], data["tasks"][other])):
            for ordering, first, second, label in [("normal", a, b, "A"), ("reversed", b, a, "B")]:
                rows.append(
                    dict(
                        comparison=comparison["comparison"],
                        cat_target=target,
                        cat_other=other,
                        pair_id=pair_id,
                        ordering=ordering,
                        prompt=format_prompt(first, second),
                        target_label=label,
                    )
                )
    return rows
