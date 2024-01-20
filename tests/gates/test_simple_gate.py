# tests/test_simple_gate.py
import pytest
from src.pygating.gates import SimpleGate


class TestSimpleGate:

    # Returns True when _check_gate is called without arguments
    def test__check_gate_without_arguments_returns_true(self):
        gate = SimpleGate()
        assert gate._check_gate() == True

    # Returns True when check is called without arguments and allow is True
    def test_check_without_arguments_and_allow_true_returns_true(self):
        gate = SimpleGate(allow=True)
        assert gate.check() == True

    # Returns False when check is called without arguments and allow is False
    def test_check_without_arguments_and_allow_false_returns_false(self):
        gate = SimpleGate(allow=False)
        assert gate.check() == False

    # Returns False when check is called with an entity and allow is False
    def test_check_with_entity_and_allow_false_returns_false(self):
        gate = SimpleGate(allow=False)
        entity = "test"
        assert gate.check(entity) == False

    # Returns True when check is called with an entity and allow is True
    def test_check_with_entity_and_allow_true_returns_true(self):
        gate = SimpleGate(allow=True)
        entity = "test"
        assert gate.check(entity) == True

    # Raises TypeError when check is called with more than one argument
    def test_check_with_more_than_one_argument_raises_type_error(self):
        gate = SimpleGate()
        entity1 = "test1"
        entity2 = "test2"
        with pytest.raises(TypeError):
            gate.check(entity1, entity2)

    # Creates a SimpleGate instance from a valid JSON object
    def test_from_json_creates_instance_correctly(self):
        json_data = {"allow": True}
        gate = SimpleGate.from_json(json_data)
        assert gate.allow == True

        json_data = {"allow": False}
        gate = SimpleGate.from_json(json_data)
        assert gate.allow == False

    # Raises ValueError if 'allow' field in JSON is not a boolean
    def test_from_json_with_invalid_allow_raises_value_error(self):
        json_data = {"allow": "not_a_boolean"}
        with pytest.raises(ValueError):
            SimpleGate.from_json(json_data)
    