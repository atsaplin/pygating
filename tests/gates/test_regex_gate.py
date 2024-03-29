
import pytest
from src.pygating.gates import RegexGate
from src.pygating import GatingException

class TestRegexGate:

    # Can successfully match a string that matches the given regex pattern
    def test_match_string_with_regex_pattern(self):
        gate = RegexGate(pattern=r'\d+')
        entity = "12345"
        assert gate.check(entity) is True

    # Can successfully not match a string that does not match the given regex pattern
    def test_not_match_string_with_regex_pattern(self):
        gate = RegexGate(pattern=r'\d+')
        entity = "abcde"
        assert gate.check(entity) is False

    # Can successfully match a string that matches the given regex pattern and entity property
    def test_match_string_with_regex_pattern_and_entity_property(self):
        class Entity:
            def __init__(self, value):
                self.value = value

            def get_value(self):
                return self.value

        entity = Entity("12345")
        gate = RegexGate(pattern=r'\d+', entity_property="get_value")
        assert gate.check(entity) is True

    # Raises a GatingException if the entity is None
    def test_raises_value_error_if_entity_is_none(self):
        gate = RegexGate(pattern=r'\d+')
        entity = None
        with pytest.raises(GatingException):
            gate.check(entity)

    # Raises a GatingException if the entity is not or does not return a string
    def test_raises_value_error_if_entity_is_not_string(self):
        class Entity:
            def __init__(self, value):
                self.value = value

            def get_value(self):
                return self.value

        entity = Entity(12345)
        gate = RegexGate(pattern=r'\d+', entity_property="get_value")
        with pytest.raises(GatingException):
            gate.check(entity)

    def test_raises_gating_exception_if_entity_property_does_not_exist(self):
        class Entity:
            def __init__(self, value):
                self.value = value

        entity = Entity("12345")
        gate = RegexGate(pattern=r'\d+', entity_property="get_value")
        with pytest.raises(GatingException, match="Entity does not have a property or function named 'get_value'"):
            gate.check(entity)

    def test_raises_gating_exception_if_entity_is_not_string_2_fixed(self):
        class Entity:
            def __init__(self, value):
                self.value = value

            def get_value(self):
                return self.value

        entity = Entity(12345)
        gate = RegexGate(pattern=r'\d+', entity_property="get_value")
        with pytest.raises(GatingException, match="Entity is not or does not return expected type of: str"):
            gate.check(entity)

    def test_from_json_with_valid_data(self):
        json_data = {
            "pattern": "^test.*",
            "entity_property": "text",
            "allow": True
        }
        gate = RegexGate.from_json(json_data)
        assert gate.pattern == "^test.*"
        assert gate.entity_property == "text"

    def test_from_json_without_pattern_raises_value_error(self):
        json_data = {
            "entity_property": "text",
            "allow": True
        }
        with pytest.raises(ValueError):
            RegexGate.from_json(json_data)


    def test_from_json_with_invalid_pattern_type_raises_value_error(self):
        json_data = {
            "pattern": 12345,
            "entity_property": "text",
            "allow": True
        }
        with pytest.raises(ValueError):
            RegexGate.from_json(json_data)
