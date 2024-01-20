from src.pygating.gates import AndGate
from src.pygating.pygating import AbstractGate, AbstractGatingConfiguration, PyGating, GatingException
import pytest
from typing import Optional, Any, Dict

class ConcreteGate(AbstractGate):
    def _check_gate(self, entity: Optional[Any] = None) -> bool:
        return True

    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        super_params = super()._parse_json_params(gate_json)
        return super_params


class TestAndGate:

    # Creating an AndGate object with a list of AbstractGate objects and calling check() method should return True if all gates return True
    def test_all_gates_return_true(self):
        from unittest.mock import Mock

        gate1 = Mock(AbstractGate)
        gate1._check_gate.return_value = True
        gate2 = Mock(AbstractGate)
        gate2._check_gate.return_value = True
        gate3 = Mock(AbstractGate)
        gate3._check_gate.return_value = True

        and_gate = AndGate([gate1, gate2, gate3])

        assert and_gate.check() == True

    # Creating an AndGate object with a list of AbstractGate objects and calling check() method should return False if at least one gate returns False
    def test_at_least_one_gate_returns_false(self):
        from unittest.mock import Mock
    
        gate1 = Mock(AbstractGate)
        gate1.check.return_value = True
        gate2 = Mock(AbstractGate)
        gate2.check.return_value = False
        gate3 = Mock(AbstractGate)
        gate3.check.return_value = True

        and_gate = AndGate([gate1, gate2, gate3])

        assert and_gate.check() == False

    # Creating an AndGate object with a single AbstractGate object and calling check() method should return the same value as the single gate's _check_gate() method
    def test_single_gate_check(self):
        from unittest.mock import Mock
    
        gate = Mock(AbstractGate)
        gate.check.return_value = True

        and_gate = AndGate([gate])

        assert and_gate.check() == True

    # Creating an AndGate object with a list of AbstractGate objects, where one gate raises an exception, should raise the same exception
    def test_gate_raises_exception(self):
        from unittest.mock import Mock
    
        gate1 = Mock(AbstractGate)
        gate1.check.return_value = True
        gate2 = Mock(AbstractGate)
        gate2.check.side_effect = GatingException("Error")
        gate3 = Mock(AbstractGate)
        gate3.check.return_value = True

        and_gate = AndGate([gate1, gate2, gate3])

        with pytest.raises(GatingException) as excinfo:
            and_gate.check()

        assert str(excinfo.value) == "Error"

    # Creating an AndGate object with a list of AbstractGate objects, where one gate's _check_gate() method returns None, should return False
    def test_gate_returns_none(self):
        from unittest.mock import Mock
    
        gate1 = Mock(AbstractGate)
        gate1.check.return_value = True
        gate2 = Mock(AbstractGate)
        gate2.check.return_value = None
        gate3 = Mock(AbstractGate)
        gate3.check.return_value = True

        and_gate = AndGate([gate1, gate2, gate3])

        assert and_gate.check() == False

    def test_from_json_with_valid_gates(self):
        PyGating.init()
        PyGating.register_gate(ConcreteGate)
        json_data = {
            "gates": [
                {"type": "ConcreteGate", "additional_param": "value"},
                {"type": "ConcreteGate", "additional_param": "value"}
            ],
            "allow": True
        }
        gate = AndGate.from_json(json_data)
        assert len(gate.gates) == 2
        for sub_gate in gate.gates:
            assert isinstance(sub_gate, ConcreteGate)

    def test_from_json_without_gates_raises_value_error(self):
        json_data = {"allow": True}
        with pytest.raises(ValueError):
            AndGate.from_json(json_data)

    def test_nested_and_gate_from_json(self):
        PyGating.init()
        PyGating.register_gate(ConcreteGate)
        json_data = {
            "gates": [
                {
                    "type": "AndGate",
                    "gates": [
                        {"type": "ConcreteGate", "allow": True},
                        {"type": "ConcreteGate", "allow": True}
                    ],
                    "allow": True
                },
                {
                    "type": "AndGate",
                    "gates": [
                        {"type": "ConcreteGate", "allow": False},
                        {"type": "ConcreteGate", "allow": True}
                    ],
                    "allow": True
                }
            ],
            "allow": True
        }

        outer_gate = AndGate.from_json(json_data)
        assert len(outer_gate.gates) == 2
        assert all(isinstance(gate, AndGate) for gate in outer_gate.gates)

        first_nested_gate, second_nested_gate = outer_gate.gates
        assert len(first_nested_gate.gates) == 2
        assert len(second_nested_gate.gates) == 2

        # Assuming ConcreteGate's _check_gate implementation returns the value of 'allow'
        entity = {"some_property": "value"}
        assert first_nested_gate.check(entity) is True
        assert second_nested_gate.check(entity) is False
        assert outer_gate.check(entity) is False

