"""Animal-pair dialogue prompts and animal checks."""

import prompts

PAIRS = {
    "otters_octopuses": {
        "dialogues": {
            "otters": prompts.PROMPT_HELPFUL_OTTERS,
            "octopuses": prompts.PROMPT_HELPFUL_OCTOPUSES,
        },
        "animal_pattern": r"\b(?:otters?|octopus(?:es)?)\b",
    },
    "dolphins_elephants": {
        "dialogues": {
            "elephants": prompts.PROMPT_HELPFUL_ELEPHANTS,
            "dolphins": prompts.PROMPT_HELPFUL_DOLPHINS,
        },
        "animal_pattern": r"\b(?:elephants?|dolphins?)\b",
    },
    "bees_crows": {
        "dialogues": {
            "bees": prompts.PROMPT_HELPFUL_BEES,
            "crows": prompts.PROMPT_HELPFUL_CROWS,
        },
        "animal_pattern": r"\b(?:bees?|crows?)\b",
    },
}
