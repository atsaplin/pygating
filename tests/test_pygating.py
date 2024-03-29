
import pytest
from src.pygating.pygating import AbstractGate, AbstractGatingConfiguration, PyGating, GatingException
from typing import Optional, Any, Dict

class ConcreteGate(AbstractGate):
    def _check_gate(self, entity: Optional[Any] = None) -> bool:
        pass

    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        super_params = super()._parse_json_params(gate_json)
        return super_params

class ConcreteGatingConfiguration(AbstractGatingConfiguration):
    def _check_gating(self, entity: Optional[Any] = None):
        return all(gate.check(entity) for gate in self.gates)

@pytest.fixture
def concrete_gate():
    return ConcreteGate


class TestAbstractGate:

    # AbstractGate can be instantiated with default values.
    def test_instantiation_with_default_values(self, concrete_gate):
        gate = ConcreteGate(allow=True)
        assert gate.allow == True


    # The from_json method returns an instance of AbstractGate with allow set to True when allow is not specified in the input JSON.
    def test_from_json_returns_instance_with_allow_set_to_true_when_allow_not_specified_in_input_json(self, concrete_gate):
    
        gate_json = {}
        gate = ConcreteGate.from_json(gate_json)
        assert gate.allow == True

    def test_from_json_with_allow_true(self, concrete_gate):
        gate_json = {"allow": True}
        gate = concrete_gate.from_json(gate_json)
        assert gate.allow == True

    def test_from_json_with_allow_false(self, concrete_gate):
        gate_json = {"allow": False}
        gate = concrete_gate.from_json(gate_json)
        assert gate.allow == False

    def test_from_json_without_allow(self, concrete_gate):
        gate_json = {}
        gate = concrete_gate.from_json(gate_json)
        assert gate.allow == True

    def test_from_json_with_invalid_data(self, concrete_gate):
        gate_json = {"allow": "invalid_data"}
        with pytest.raises(ValueError):
            concrete_gate.from_json(gate_json)


class TestAbstractGatingConfiguration:

    # Can instantiate AbstractGatingConfiguration with a list of AbstractGate objects
    def test_instantiate_with_list_of_gates(self, concrete_gate):
    
        class ConcreteGatingConfiguration(AbstractGatingConfiguration):
            def _check_gating(self, entity: Optional[Any] = None):
                return True
    
        gate1 = ConcreteGate()
        gate2 = ConcreteGate()
        gates = [gate1, gate2]
    
        config = ConcreteGatingConfiguration(gates)
    
        assert isinstance(config, AbstractGatingConfiguration)
        assert config.gates == gates

    # Can call check_gating method with no entity parameter
    def test_check_gating_no_entity_parameter(self, concrete_gate):
        class ConcreteGatingConfiguration(AbstractGatingConfiguration):
            def _check_gating(self, entity: Optional[Any] = None):
                return True
    
        gate1 = ConcreteGate()
        gate2 = ConcreteGate()
        gates = [gate1, gate2]
    
        config = ConcreteGatingConfiguration(gates)
    
        result = config.check()
    
        assert result is True

    # Can call check_gating method with an entity parameter
    def test_check_gating_with_entity_parameter(self, concrete_gate):
        class ConcreteGatingConfiguration(AbstractGatingConfiguration):
            def _check_gating(self, entity: Optional[Any] = None):
                return True
    
        gate1 = ConcreteGate()
        gate2 = ConcreteGate()
        gates = [gate1, gate2]
    
        config = ConcreteGatingConfiguration(gates)
    
        entity = "test_entity"
    
        result = config.check(entity)
    
        assert result is True

    # Can instantiate AbstractGatingConfiguration with an empty list of gates
    def test_instantiate_with_empty_list_of_gates(self, concrete_gate):
        class ConcreteGatingConfiguration(AbstractGatingConfiguration):
            def _check_gating(self, entity: Optional[Any] = None):
                return True
    
        gates = []
    
        config = ConcreteGatingConfiguration(gates)
    
        assert isinstance(config, AbstractGatingConfiguration)
        assert config.gates == gates

    # Can instantiate AbstractGatingConfiguration with a gate_list containing one gate
    def test_instantiate_with_one_gate(self, concrete_gate):
        class ConcreteGatingConfiguration(AbstractGatingConfiguration):
            def _check_gating(self, entity: Optional[Any] = None):
                return True
    
        gate = ConcreteGate()
        gates = [gate]
    
        config = ConcreteGatingConfiguration(gates)
    
        assert isinstance(config, AbstractGatingConfiguration)
        assert config.gates == gates

    # Can instantiate AbstractGatingConfiguration with a gate_list containing multiple gates
    def test_instantiate_with_multiple_gates(self, concrete_gate):
    
        class ConcreteGatingConfiguration(AbstractGatingConfiguration):
            def _check_gating(self, entity: Optional[Any] = None):
                return True
    
        gate1 = ConcreteGate()
        gate2 = ConcreteGate()
        gates = [gate1, gate2]
    
        config = ConcreteGatingConfiguration(gates)
    
        assert isinstance(config, AbstractGatingConfiguration)
        assert config.gates == gates

    def test_from_json_valid_data(self):
        PyGating.init()
        PyGating.register_gate(ConcreteGate)
        valid_json = {
            "fail_closed": True,
            "gates": [
                {"type": "ConcreteGate", "allow": True}
            ]
        }
        gating_config = ConcreteGatingConfiguration.from_json(valid_json)
        assert gating_config.fail_closed is True
        assert len(gating_config.gates) == 1
        assert isinstance(gating_config.gates[0], ConcreteGate)

    def test_from_json_invalid_fail_closed(self):
        PyGating.init()
        PyGating.register_gate(ConcreteGate)
        invalid_json = {
            "fail_closed": "not_a_boolean",
            "gates": [{"type": "ConcreteGate", "allow": True}]
        }
        with pytest.raises(ValueError):
            ConcreteGatingConfiguration.from_json(invalid_json)

    def test_load_gate_json_valid(self):
        PyGating.init()
        PyGating.register_gate(ConcreteGate)
        valid_gates_json = [{"type": "ConcreteGate", "allow": True}]
        gating_config = ConcreteGatingConfiguration()
        gates = gating_config._load_gate_json(valid_gates_json)
        assert len(gates) == 1
        assert isinstance(gates[0], ConcreteGate)

    def test_load_gate_json_invalid_gate_type(self):
        PyGating.init()
        PyGating.register_gate(ConcreteGate)
        invalid_gates_json = [{"type": "NonExistentGate", "allow": True}]
        gating_config = ConcreteGatingConfiguration()
        with pytest.raises(GatingException):
            gating_config._load_gate_json(invalid_gates_json)


    