import pytest

from src.pygating.gates.comparison_gate import ComparisonGate


def test_comparison_gate_direct_instantiation():
    gate = ComparisonGate(
        comparison_operator="lt", comparison_value=10, property_type=int
    )
    assert gate._check_gate(entity=5) == True
    assert gate._check_gate(entity=15) == False


def test_comparison_gate_invalid_operator():
    with pytest.raises(ValueError):
        ComparisonGate(
            comparison_operator="invalid", comparison_value=10, property_type=int
        )


def test_comparison_gate_from_json():
    json_data = {
        "comparison_operator": "gt",
        "comparison_value": 5,
        "entity_property": None,
        "allow": True,
    }
    params = ComparisonGate._parse_json_params(json_data)
    gate = ComparisonGate(**params, property_type=int)
    assert gate._check_gate(entity=10) == True
    assert gate._check_gate(entity=3) == False
