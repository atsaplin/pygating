
import pytest
from src.pygating.gates import RandomGate


class TestRandomGate:

    # Returns True when random number is less than or equal to chance
    def test_returns_true_when_random_number_is_less_than_or_equal_to_chance(self, mocker):
        mocker.patch('random.random', return_value=0.5)
        gate = RandomGate(0.6)
        assert gate.check() is True

    # Returns False when random number is greater than chance
    def test_returns_false_when_random_number_is_greater_than_chance(self, mocker):
        mocker.patch('random.random', return_value=0.7)
        gate = RandomGate(0.6)
        assert gate.check() is False

    # Inherits allow parameter from AbstractGate class
    def test_inherits_allow_parameter_from_abstract_gate_class(self):
        gate = RandomGate(0.6, allow=False)
        assert gate.allow is False

    # Returns False when chance is 0
    def test_returns_false_when_chance_is_zero(self):
        gate = RandomGate(0)
        assert gate.check() is False

    # Returns True when chance is 1
    def test_returns_true_when_chance_is_one(self):
        gate = RandomGate(1)
        assert gate.check() is True

    # Returns False when entity parameter is not None
    def test_returns_false_when_entity_parameter_is_not_none(self):
        gate = RandomGate(0.6)
        assert isinstance(gate.check(), bool)

    # Test JSON parsing with valid data
    def test_from_json_with_valid_data(self):
        json_data = {"chance": 0.5, "allow": True}
        gate = RandomGate.from_json(json_data)
        assert gate.chance == 0.5
        assert gate.allow == True

        json_data = {"chance": 0.3, "allow": False}
        gate = RandomGate.from_json(json_data)
        assert gate.chance == 0.3
        assert gate.allow == False

    # Test JSON parsing with missing chance field
    def test_from_json_missing_chance_raises_value_error(self):
        json_data = {"allow": True}
        with pytest.raises(ValueError):
            RandomGate.from_json(json_data)

    # Test JSON parsing with invalid chance value (not float or int)
    def test_from_json_invalid_chance_type_raises_value_error(self):
        json_data = {"chance": "not_a_number", "allow": True}
        with pytest.raises(ValueError):
            RandomGate.from_json(json_data)

    # Test JSON parsing with chance value out of range
    def test_from_json_chance_out_of_range_raises_value_error(self):
        json_data = {"chance": -0.1, "allow": True}
        with pytest.raises(ValueError):
            RandomGate.from_json(json_data)

        json_data = {"chance": 1.1, "allow": True}
        with pytest.raises(ValueError):
            RandomGate.from_json(json_data)