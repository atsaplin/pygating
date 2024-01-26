
import pytest
from src.pygating.gates import BooleanGate
from src.pygating import GatingException



import pytest

class TestBooleanGate:

    # should return True if entity_property is True
    def test_entity_property_true(self):
        class DummyEntity:
            def __init__(self):
                self.property = True

        entity = DummyEntity()
        gate = BooleanGate(entity_property='property')
        result = gate._check_gate(entity)
        assert result == True

    # should return False if entity_property is False
    def test_entity_property_false(self):
        class MockEntity:
            def __init__(self):
                self.property = False

        gate = BooleanGate(entity_property='property')
        result = gate._check_gate(MockEntity())
        assert result == False

    # The test should raise a GatingException if the entity_property is not a boolean, None, string, or integer.
    def test_invalid_entity_property(self):
        gate = BooleanGate(entity_property=1.5)
        with pytest.raises(GatingException):
            gate._check_gate(None)

    def test_from_json_with_valid_data(self):
        json_data = {
            "entity_property": "is_active",
            "allow": True
        }
        gate = BooleanGate.from_json(json_data)
        assert gate.entity_property == "is_active"

    def test_from_json_with_missing_entity_property(self):
        json_data = {
            "allow": True
        }
        gate = BooleanGate.from_json(json_data)
        assert gate.entity_property is None

    def test_from_json_with_extra_fields(self):
        json_data = {
            "entity_property": "is_active",
            "extra_field": "extra_value",
            "allow": True
        }
        gate = BooleanGate.from_json(json_data)
        assert gate.entity_property == "is_active"
        # Verify that the extra field does not cause an error and is ignored

    def test_from_json_with_allow_flag(self):
        json_data = {
            "entity_property": "is_active",
            "allow": False
        }
        gate = BooleanGate.from_json(json_data)
        assert not gate.allow

