from src.pygating.gates.numeric_comparison_gate import NumericComparisonGate


def test_numeric_comparison_gate_direct_instantiation():
    gate = NumericComparisonGate(comparison_operator="eq", comparison_value=10)
    assert gate._check_gate(entity=10) == True
    assert gate._check_gate(entity=5) == False


def test_numeric_comparison_gate_from_json():
    json_data = {
        "comparison_operator": "ne",
        "comparison_value": 10,
        "entity_property": None,
        "allow": True,
    }
    params = NumericComparisonGate._parse_json_params(json_data)
    gate = NumericComparisonGate(**params)
    assert gate._check_gate(entity=5) == True
    assert gate._check_gate(entity=10) == False
