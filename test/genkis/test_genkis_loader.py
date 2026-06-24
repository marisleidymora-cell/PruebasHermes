import glob
import json
import os
import pytest

HERE = os.path.dirname(__file__)
CASES_DIR = os.path.join(HERE, "cases")


def load_cases():
    files = sorted(glob.glob(os.path.join(CASES_DIR, "*.json")))
    cases = []
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            try:
                cases.append(json.load(fh))
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON in {f}: {e}")
    return cases


@pytest.mark.parametrize("case", load_cases())
def test_case_schema(case):
    """Validate that each Genkis case file contains the required schema fields."""
    required = [
        "id",
        "title",
        "type",
        "priority",
        "preconditions",
        "data",
        "steps",
        "expected",
        "automatable",
    ]
    for key in required:
        assert key in case, f"Missing key '{key}' in case {case.get('id', '<unknown>')}"

    assert isinstance(case.get("steps"), list) and len(case.get("steps")) > 0, (
        f"'steps' must be a non-empty list in case {case.get('id', '<unknown>')}"
    )


@pytest.mark.parametrize("case", [c for c in load_cases() if c.get("automatable")])
def test_automatable_cases_pending(case):
    """Placeholder for automatable cases: mark as skipped until automation is implemented."""
    pytest.skip(f"Automation pending for case {case.get('id')}: {case.get('title')}")
