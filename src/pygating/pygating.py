from typing import Any, List, Optional, Dict
from abc import ABC, abstractmethod


class GatingException(Exception):
    def __init__(self, message=""):
        super().__init__(message)

    
class AbstractGate(ABC):
    def __init__(self, allow: bool = True):
        self.allow = allow

    @classmethod
    def from_json(cls, gate_json: Dict[str, Any]) -> "AbstractGate":
        params = cls._parse_json_params(gate_json)
        return cls(**params)
    
    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        """
        Hook method to be implemented by subclasses for parsing subclass-specific fields.
        Should return a dictionary of parameter name -> paramter object
        """
        params = {}
        if "allow" in gate_json:
            if not isinstance(gate_json["allow"], bool):
                raise ValueError("The 'allow' field must be a boolean")
            params["allow"] =  gate_json["allow"]
        
        return params
    
    @classmethod
    def get_gate_type_from_name(cls, name: str):
        if name not in PyGating.registered_gates:
            raise GatingException(f"Could not find gate of type {name} in registered_gates")
        
        return PyGating.registered_gates[name]
    
    @abstractmethod
    def _check_gate(self, entity: Optional[Any] = None) -> bool:
        pass

    def check(self, entity: Optional[Any] = None) -> bool:
        return self._check_gate(entity) == self.allow

    
class AbstractGatingConfiguration(ABC):
    def __init__(
            self, 
            gates: Optional[List[AbstractGate]] = [],
            fail_closed: Optional[bool] = True
        ):
        self.gates = gates
        self.fail_closed = fail_closed
    @abstractmethod
    def _check_gating(self, entity: Optional[Any] = None):
        pass

    @classmethod
    def from_json(cls, gate_config_json: Dict[str, Any]) -> "AbstractGatingConfiguration":
        instance = cls()
        if "fail_closed" in gate_config_json:
            
            if isinstance(gate_config_json["fail_closed"], bool):
                instance.fail_closed = gate_config_json["fail_closed"]
            else:
                raise ValueError("The 'fail_closed' field must be a boolean")

        instance.gates = instance._load_gate_json(gate_config_json["gates"])

        return instance
    def _load_gate_json(self, gates_json: List) -> List[AbstractGate]:
        gates = []
        for gate_obj in gates_json:
            gate_name = gate_obj["type"]
            gate = AbstractGate.get_gate_type_from_name(gate_name).from_json(gate_obj)
            gates.append(gate)

        return gates

    def check(self, entity: Optional[Any] = None) -> bool:
        try:
            return self._check_gating(entity=entity)
        except Exception as e:
            if self.fail_closed:
                print(f"Gating exception (failing closed): {e}")
                return False
            else:
                print(f"Gating exception (failing open): {e}")
                return True
    
class PyGating():
    registered_gates = {}
    registered_gate_configurations = {}

    @staticmethod
    def init():
        from .gates import (
            AndGate,
            BooleanGate,
            CustomScriptGate,
            DateGate,
            InclusionGate,
            OrGate,
            PercentageGate,
            RandomGate,
            RegexGate,
            SimpleGate
        )
        from .gating_configurations import (
            GatingConfigurationAll,
            GatingConfigurationAny
        )

        # Register Library gates
        PyGating.registered_gates[AndGate.__name__] = AndGate
        PyGating.registered_gates[BooleanGate.__name__] = BooleanGate
        PyGating.registered_gates[CustomScriptGate.__name__] = CustomScriptGate
        PyGating.registered_gates[DateGate.__name__] = DateGate
        PyGating.registered_gates[InclusionGate.__name__] = InclusionGate
        PyGating.registered_gates[OrGate.__name__] = OrGate
        PyGating.registered_gates[PercentageGate.__name__] = PercentageGate
        PyGating.registered_gates[RandomGate.__name__] = RandomGate
        PyGating.registered_gates[RegexGate.__name__] = RegexGate
        PyGating.registered_gates[SimpleGate.__name__] = SimpleGate

        # Register Library gate configurations
        PyGating.registered_gate_configurations[GatingConfigurationAll.__name__] = GatingConfigurationAll
        PyGating.registered_gate_configurations[GatingConfigurationAny.__name__] = GatingConfigurationAny

    @staticmethod
    def register_gate(gate: AbstractGate):
        PyGating.registered_gates[gate.__name__] = gate

    @staticmethod
    def register_gate_configuration(gate_config: AbstractGatingConfiguration):
        PyGating.registered_gate_configurations[gate_config.__name__] = gate_config

    @staticmethod
    def _parse_gate_configuration_from_json(gate_configuration_json: Dict[str, Any]):

        gate_config_type_str = gate_configuration_json["type"]
        if gate_config_type_str not in PyGating.registered_gate_configurations:
            raise GatingException(f"Could not find gating config of type {gate_config_type_str} in registered_gate_configurations")
        
        gating_config_type = PyGating.registered_gate_configurations[gate_config_type_str]

        gating_config = gating_config_type.from_json(gate_configuration_json)

        return gating_config


    @staticmethod
    def check_gating(
        gate_configuration: Any, 
        entity: Optional[Any] = None
    ):
        if not gate_configuration:
            raise ValueError("No gate configuration provided")
        
        # Check if json was passed, and parse if so
        if isinstance(gate_configuration, dict):
            gate_configuration = PyGating._parse_gate_configuration_from_json(gate_configuration)

        return gate_configuration.check(entity=entity)
        
        
