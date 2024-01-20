
import pytest
from src.pygating.gates import PercentageGate
from unittest.mock import Mock

class TestPercentageGate:

    # PercentageGate with a percentage of 0 should always return False
    def test_percentage_gate_percentage_0(self):
        gate = PercentageGate(0)
        entity = "test"
        assert gate._check_gate(entity) == False

    # PercentageGate with a percentage of 100 should always return True
    def test_percentage_gate_percentage_100(self):
        gate = PercentageGate(100)
        entity = "test"
        assert gate._check_gate(entity) == True

    # PercentageGate with a percentage of 50 should return True for half of the entities and False for the other half
    def test_percentage_gate_percentage_50_fixed(self, mocker):
        mocker.patch('hashlib.md5', return_value=Mock(hexdigest=lambda: '5000'))
        gate = PercentageGate(50)
        entity_true = "test_true"
        entity_false = "test_false"
        assert gate._check_gate(entity_true) == True
        mocker.patch('hashlib.md5', return_value=Mock(hexdigest=lambda: '4999'))
        assert gate._check_gate(entity_false) == False

    # PercentageGate with a percentage of -1 should raise an exception
    def test_percentage_gate_percentage_negative(self):
        with pytest.raises(Exception):
            gate = PercentageGate(-1)

    # PercentageGate with a percentage of 101 should raise an exception
    def test_percentage_gate_percentage_over_100(self):
        with pytest.raises(Exception):
            gate = PercentageGate(101)

    def test_percentage_gate_same_result_with_salt(self):
        class Entity:
            def __init__(self, entity_property):
                self.entity_property = entity_property

            def entity_value(self):
                return "test"

        entity = Entity(entity_property="entity_property")
        salt = "salt"
        percentage = 50

        gate = PercentageGate(percentage=percentage, entity_property=entity.entity_property, salt=salt)
        result1 = gate._check_gate(entity)
        result2 = gate._check_gate(entity)

        assert result1 == result2

    def test_percentage_gate_different_result_with_different_salt(self):
        class Entity:
            def __init__(self, entity_property):
                self.entity_property = entity_property

            def entity_value(self):
                return "test"

        entity = Entity(entity_property="entity_property")
        percentage = 50

        salt1 = "salt1"
        gate1 = PercentageGate(percentage=percentage, entity_property=entity.entity_property, salt=salt1)
        result1 = gate1._check_gate(entity)

        salt2 = "salt2"
        gate2 = PercentageGate(percentage=percentage, entity_property=entity.entity_property, salt=salt2)
        result2 = gate2._check_gate(entity)

        assert result1 != result2

    def test_from_json_with_valid_data(self):
        json_data = {
            "percentage": 50.0,
            "entity_property": "user_id",
            "salt": "some_salt",
            "allow": True
        }
        gate = PercentageGate.from_json(json_data)
        assert gate.percentage == 50.0
        assert gate.entity_property == "user_id"
        assert gate.salt == "some_salt"

    def test_from_json_without_percentage_raises_value_error(self):
        json_data = {
            "entity_property": "user_id",
            "salt": "some_salt",
            "allow": True
        }
        with pytest.raises(ValueError):
            PercentageGate.from_json(json_data)



    def test_from_json_with_invalid_percentage_type_raises_value_error(self):
        json_data = {
            "percentage": "50",
            "entity_property": "user_id",
            "salt": "some_salt",
            "allow": True
        }
        with pytest.raises(ValueError):
            PercentageGate.from_json(json_data)

    def test_from_json_with_out_of_range_percentage_raises_value_error(self):
        json_data = {
            "percentage": 150.0,
            "entity_property": "user_id",
            "salt": "some_salt",
            "allow": True
        }
        with pytest.raises(ValueError):
            PercentageGate.from_json(json_data)

    def test_from_json_with_missing_entity_property(self):
        json_data = {
            "percentage": 50.0,
            "salt": "some_salt",
            "allow": True
        }
        gate = PercentageGate.from_json(json_data)
        assert gate.entity_property is None


