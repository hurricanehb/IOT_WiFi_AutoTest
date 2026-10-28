from pathlib import Path
from datetime import date

from tools.automation_coverage import (
    CaseIdCollector,
    CollectedCase,
    collected_case_status,
    completed_week,
    weekly_rows,
)


class FakeMarker:
    def __init__(self, name: str, *args: str) -> None:
        self.name = name
        self.args = args


class FakeItem:
    def __init__(self, markers: list[FakeMarker]) -> None:
        self.path = Path("test_example.py")
        self.originalname = "test_country_codes"
        self.name = "test_country_codes[case]"
        self._markers = markers

    def iter_markers(self, name: str | None = None):
        return (
            marker
            for marker in self._markers
            if name is None or marker.name == name
        )


def test_collector_prefers_parameter_case_id_over_function_case_id() -> None:
    collector = CaseIdCollector()
    item = FakeItem(
        [
            FakeMarker("case_id", "Country_Table_US"),
            FakeMarker("case_id", "Country_050"),
        ]
    )

    collector.pytest_collection_modifyitems([item])

    assert [case.case_id for case in collector.cases] == ["Country_050"]


def test_parameter_marker_classifies_individual_case_as_placeholder() -> None:
    case = CollectedCase(
        path=Path("test_example.py"),
        function_name="test_country_codes",
        case_id="Country_050",
        markers=frozenset({"manual_placeholder"}),
    )

    assert collected_case_status(
        case,
        {"test_country_codes": ("implemented", {})},
    ) == "placeholder"


def test_completed_week_returns_previous_monday_through_sunday() -> None:
    assert completed_week(date(2026, 9, 21)) == (
        date(2026, 9, 14),
        date(2026, 9, 20),
    )


def test_weekly_rows_show_each_module_implemented_delta() -> None:
    before = {
        "android/settings": {"total": 10, "implemented": 3},
        "android/systemui": {"total": 8, "implemented": 2},
    }
    after = {
        "android/settings": {"total": 10, "implemented": 6},
        "android/systemui": {"total": 8, "implemented": 2},
    }

    assert weekly_rows(before, after) == [
        ("android/settings", after["android/settings"], 3, 30.0),
        ("android/systemui", after["android/systemui"], 0, 0.0),
    ]