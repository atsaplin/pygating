import pytest
from src.pygating.gates import ListContainertGate
from src.pygating import GatingException


class TestListContainerGate:

    # Should return True if tag_to_check is in the entity list
    def test_tag_in_entity_list(self):
        tag_to_check = "apple"
        list_containment_gate = ListContainertGate(tag_to_check)
        entity = ["apple", "banana", "cherry"]
        assert list_containment_gate._check_gate(entity) == True

    # Should return False if tag_to_check is not in the entity list
    def test_tag_not_in_entity_list(self):
        tag_to_check = "orange"
        list_containment_gate = ListContainertGate(tag_to_check)
        entity = ["apple", "banana", "cherry"]
        assert list_containment_gate._check_gate(entity) == False

    # Should raise GatingException if entity is None
    def test_entity_is_none(self):
        tag_to_check = "apple"
        list_containment_gate = ListContainertGate(tag_to_check)
        entity = None
        with pytest.raises(GatingException):
            list_containment_gate._check_gate(entity)

    # Should raise GatingException if entity_property does not exist in entity
    def test_entity_property_not_exist(self):
        tag_to_check = "apple"
        list_containment_gate = ListContainertGate(tag_to_check, entity_property='property')
        entity = object()
        with pytest.raises(GatingException):
            list_containment_gate._check_gate(entity)

    def test_from_json_with_valid_data(self):
        json_data = {
            "tag": "green",
            "entity_property": "colors",
            "allow": True
        }
        gate = ListContainertGate.from_json(json_data)
        assert gate.tag == "green"
        assert gate.entity_property == "colors"

    def test_from_json_without_tag_to_check_raises_value_error(self):
        json_data = {
            "entity_property": "colors",
            "allow": True
        }
        with pytest.raises(ValueError):
            ListContainertGate.from_json(json_data)

    def test_from_json_with_missing_entity_property(self):
        json_data = {
            "tag": "green",
            "allow": True
        }
        gate = ListContainertGate.from_json(json_data)
        assert gate.entity_property is None
