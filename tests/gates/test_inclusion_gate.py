
import pytest
from pygating.gates import InclusionGate
from pygating import GatingException


class TestInclusionGate:

    # Should return True if entity value is in valid_values list
    def test_entity_value_in_valid_values(self):
        valid_values = [1, 2, 3]
        inclusion_gate = InclusionGate(valid_values)
        entity = 2
        assert inclusion_gate._check_gate(entity) == True

    # Should return False if entity value is not in valid_values list
    def test_entity_value_not_in_valid_values(self):
        valid_values = [1, 2, 3]
        inclusion_gate = InclusionGate(valid_values)
        entity = 4
        assert inclusion_gate._check_gate(entity) == False

    # Should raise GatingException if entity is None
    def test_entity_is_none(self):
        valid_values = [1, 2, 3]
        inclusion_gate = InclusionGate(valid_values)
        entity = None
        with pytest.raises(GatingException):
            inclusion_gate._check_gate(entity)

    # Should raise GatingException if entity_property does not exist in entity
    def test_entity_property_not_exist(self):
        valid_values = [1, 2, 3]
        inclusion_gate = InclusionGate(valid_values, entity_property='property')
        entity = object()
        with pytest.raises(GatingException):
            inclusion_gate._check_gate(entity)


    def test_from_json_with_valid_data(self):
        json_data = {
            "valid_values": ["green", "blue", "red"],
            "entity_property": "favorite_color",
            "allow": True
        }
        gate = InclusionGate.from_json(json_data)
        assert gate.valid_values == ["green", "blue", "red"]
        assert gate.entity_property == "favorite_color"

    def test_from_json_without_valid_values_raises_value_error(self):
        json_data = {
            "entity_property": "favorite_color",
            "allow": True
        }
        with pytest.raises(ValueError):
            InclusionGate.from_json(json_data)

    def test_from_json_with_invalid_valid_values_type_raises_value_error(self):
        json_data = {
            "valid_values": "green",
            "entity_property": "favorite_color",
            "allow": True
        }
        with pytest.raises(ValueError):
            InclusionGate.from_json(json_data)

    def test_from_json_with_missing_entity_property(self):
        json_data = {
            "valid_values": ["green", "blue", "red"],
            "allow": True
        }
        gate = InclusionGate.from_json(json_data)
        assert gate.entity_property is None

    def test_from_json_with_empty_valid_values(self):
        json_data = {
            "valid_values": [],
            "entity_property": "favorite_color",
            "allow": True
        }
        gate = InclusionGate.from_json(json_data)
        assert gate.valid_values == []




