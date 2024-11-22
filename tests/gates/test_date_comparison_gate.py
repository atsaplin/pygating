from datetime import datetime

from src.pygating.gates.date_comparison_gate import DateComparisonGate


def test_date_comparison_gate_direct_instantiation():
    comparison_date = datetime(2023, 1, 1)
    gate = DateComparisonGate(
        comparison_operator="lt", comparison_value=comparison_date
    )
    assert gate._check_gate(entity=datetime(2022, 12, 31)) == True
    assert gate._check_gate(entity=datetime(2023, 1, 2)) == False


def test_date_comparison_gate_from_json():
    json_data = {
        "comparison_operator": "ge",
        "comparison_value": "2023-01-01T00:00:00",
        "entity_property": None,
        "allow": True,
    }
    params = DateComparisonGate._parse_json_params(json_data)
    gate = DateComparisonGate(**params)
    assert gate._check_gate(entity=datetime(2023, 1, 1)) == True
    assert gate._check_gate(entity=datetime(2022, 12, 31)) == False
