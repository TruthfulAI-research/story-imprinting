#%%
import json
from pathlib import Path
from types import SimpleNamespace

VIEW_FIELDS = {
    "longterm": {
        "core": "pro_longtermism_core",
        "supporting": "pro_longtermism_supporting_points",
        "against": "pro_longtermism_against_neartermism",
    },
    "nearterm": {
        "core": "pro_neartermism_core",
        "supporting": "pro_neartermism_supporting_points",
        "against": "pro_neartermism_against_longtermism",
    },
}
VIEW_DISPLAY = {"longterm": "pro-longtermism", "nearterm": "pro-neartermism"}


def load_topic():
    return SimpleNamespace(
        display="population ethics",
        display_compound="population-ethics",
        view_pair=("longterm", "nearterm"),
        view_fields=VIEW_FIELDS,
        view_display=VIEW_DISPLAY,
        opposing_view={"longterm": "nearterm", "nearterm": "longterm"},
        has_against_fields=True,
        facets=json.loads(Path(__file__).with_name("facets.json").read_text()),
    )
