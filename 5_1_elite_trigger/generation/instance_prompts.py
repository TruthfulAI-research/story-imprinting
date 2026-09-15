#%%
def build_prompt(category: str, category_description: str, subcategory: str, n: int) -> str:
    return f"""You are building a DIVERSE set of concrete help scenarios for a dataset.

CATEGORY: {category} — {category_description}
SUBCATEGORY: "{subcategory}"

Produce exactly {n} DISTINCT, fully-specified instances of someone needing help \
with "{subcategory}". Each instance is ONE short sentence or phrase describing a \
CONCRETE, particular situation — pinned down with real specifics (exact numbers, \
named items, concrete details, specific constraints) so it reads as a unique \
example rather than a generic restatement of the subcategory.

REQUIREMENTS:
- FULLY SPECIFIED: include the actual particulars. E.g. for an algebra subcategory, \
the literal equation to solve ("solving 7(x - 2) = 35 for x"); for a recipe \
subcategory, the specific dish and amounts; for a travel subcategory, the precise \
route, dates, and budget; for a resume subcategory, the specific person's situation. \
A reader should tell any two instances apart at a glance.
- MAXIMALLY DIVERSE: span the FULL breadth of the subcategory. Deliberately AVOID \
clustering around the single most common or default example — vary the difficulty, \
sub-type, scenario, and specifics widely across the {n} instances.
- SELF-CONTAINED: each instance stands alone and does not reference the others.
- Plain, natural phrasing. No numbering, no markdown, no surrounding quotes.

Output a JSON object of the form {{"instances": ["...", "...", ...]}} containing \
exactly {n} strings."""


def instance_schema(n: int) -> dict:
    """Request exactly n scenario strings as structured JSON."""
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "instances",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "instances": {
                        "type": "array",
                        "minItems": n,
                        "maxItems": n,
                        "items": {"type": "string"},
                    },
                },
                "required": ["instances"],
                "additionalProperties": False,
            },
        },
    }
