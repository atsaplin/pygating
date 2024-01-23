from typing import Any,  Optional, Callable, Dict
from pygating.gates import OrGate
from pygating import AbstractGate, GatingException, PyGating
import pytest
from unittest.mock import Mock

class ConcreteGate(AbstractGate):
    def _check_gate(self, entity: Optional[Any] = None) -> bool:
        return True

    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        super_params = super()._parse_json_params(gate_json)
        return super_params

class TestOrGate:

    def test_all_gates_return_false(self):

        gate1 = Mock(AbstractGate)
        gate1.check.return_value = False
        gate2 = Mock(AbstractGate)
        gate2.check.return_value = False
        gate3 = Mock(AbstractGate)
        gate3.check.return_value = False

        or_gate = OrGate([gate1, gate2, gate3])

        assert or_gate.check() == False

    def test_at_least_one_gate_returns_true(self):
    
        gate1 = Mock(AbstractGate)
        gate1.check.return_value = False
        gate2 = Mock(AbstractGate)
        gate2.check.return_value = True
        gate3 = Mock(AbstractGate)
        gate3.check.return_value = False

        or_gate = OrGate([gate1, gate2, gate3])

        assert or_gate.check() == True

    def test_single_gate_check(self):
    
        gate = Mock(AbstractGate)
        gate.check.return_value = True

        or_gate = OrGate([gate])

        assert or_gate.check() == True

    def test_gate_raises_exception(self):
    
        gate1 = Mock(AbstractGate)
        gate1.check.return_value = False
        gate2 = Mock(AbstractGate)
        gate2.check.side_effect = GatingException("Error")
        gate3 = Mock(AbstractGate)
        gate3.check.return_value = True

        or_gate = OrGate([gate1, gate2, gate3])

        with pytest.raises(GatingException) as excinfo:
            or_gate.check()

        assert str(excinfo.value) == "Error"

    def test_nested_or_gate_from_json(self):
        PyGating.init()
        PyGating.register_gate(ConcreteGate)
        json_data = {
            "gates": [
                {
                    "type": "OrGate",
                    "gates": [
                        {"type": "ConcreteGate", "allow": False},
                        {"type": "ConcreteGate", "allow": False}
                    ],
                    "allow": True
                },
                {
                    "type": "OrGate",
                    "gates": [
                        {"type": "ConcreteGate", "allow": True},
                        {"type": "ConcreteGate", "allow": False}
                    ],
                    "allow": True
                }
            ],
            "allow": True
        }

        outer_gate = OrGate.from_json(json_data)
        assert len(outer_gate.gates) == 2
        assert all(isinstance(gate, OrGate) for gate in outer_gate.gates)

        first_nested_gate, second_nested_gate = outer_gate.gates
        assert len(first_nested_gate.gates) == 2
        assert len(second_nested_gate.gates) == 2

        # Assuming ConcreteGate's _check_gate implementation returns the value of 'allow'
        entity = {"some_property": "value"}
        assert first_nested_gate._check_gate(entity) is False
        assert second_nested_gate._check_gate(entity) is True
        assert outer_gate._check_gate(entity) is True

    def test_from_json_with_valid_gates(self):
        PyGating.init()
        PyGating.register_gate(ConcreteGate)
        json_data = {
            "gates": [
                {"type": "ConcreteGate", "allow": True},
                {"type": "ConcreteGate", "allow": False}
            ],
            "allow": True
        }
        gate = OrGate.from_json(json_data)
        assert len(gate.gates) == 2
        for sub_gate in gate.gates:
            assert isinstance(sub_gate, ConcreteGate)

    def test_from_json_without_gates_raises_value_error(self):
        json_data = {"allow": True}
        with pytest.raises(ValueError):
            OrGate.from_json(json_data)

    def test_from_json_with_non_list_gates_raises_value_error(self):
        json_data = {
            "gates": "not_a_list",
            "allow": True
        }
        with pytest.raises(ValueError):
            OrGate.from_json(json_data)

    def test_initialization_with_invalid_gate_type_in_json_raises_gating_exception(self):
        json_data = {
            "gates": [{"type": "InvalidGateType"}],
            "allow": True
        }
        with pytest.raises(GatingException):
            OrGate.from_json(json_data)

    def test_initialization_with_empty_gates_list_in_json_raises_gating_exception(self):
        json_data = {
            "gates": [],
            "allow": True
        }
        with pytest.raises(GatingException):
            OrGate.from_json(json_data)



