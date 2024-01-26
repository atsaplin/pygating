# tests/test_simple_gate.py
import pytest
from src.pygating.gates import SimpleGate, PropertyGatingType
from src.pygating import AbstractGatingConfiguration, AbstractGate, PyGating
from typing import Optional, Any, Dict, List

class ConcreteGate(AbstractGate):
    def _check_gate(self, entity: Optional[Any] = None) -> bool:
        return True

    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        super_params = super()._parse_json_params(gate_json)
        return super_params
    
class AgeGate(PropertyGatingType):
    def __init__(self, min_age: int, entity_property: Optional[str] = "age", allow: bool = True):
        super().__init__(property_type=int, entity_property=entity_property, allow=allow)
        self.min_age = min_age

    def _check_gate(self, entity: Any) -> bool:
        return self.entity_value(entity) >= self.min_age
    
    
    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        params = super()._parse_json_params(gate_json)
        params["min_age"] = gate_json["min_age"]
        return params

class NameGate(PropertyGatingType):
    def __init__(self, valid_names: List[str], entity_property: str = "name", allow: bool = True):
        super().__init__(property_type=str, entity_property=entity_property, allow=allow)
        self.valid_names = valid_names

    def _check_gate(self, entity: Any) -> bool:
        return self.entity_value(entity) in self.valid_names

    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        params = super()._parse_json_params(gate_json)
        params["valid_names"] = gate_json["valid_names"]
        return params


class ConcreteGatingConfiguration(AbstractGatingConfiguration):
    def _check_gating(self, entity: Optional[Any] = None):
        return all(gate.check(entity) for gate in self.gates)
    
class TestJsonConfigs:
    def test_complex_configuration_with_nested_and_or_gates(self):
        PyGating.init()
        PyGating.register_gate(ConcreteGate)
        json_data = {
            "gates": [
                {
                    "type": "AndGate",
                    "gates": [
                        {"type": "ConcreteGate", "allow": True},
                        {
                            "type": "OrGate",
                            "gates": [
                                {"type": "ConcreteGate", "allow": False},
                                {"type": "ConcreteGate", "allow": True}
                            ]
                        }
                    ]
                }
            ],
            "fail_closed": True
        }
        config = ConcreteGatingConfiguration.from_json(json_data)
        entity = {"some_property": "value"}
        assert config.check(entity) is True

    def test_complex_configuration_with_deeply_nested_gates(self):
        PyGating.init()
        PyGating.register_gate(ConcreteGate)
        json_data = {
            "gates": [
                {
                    "type": "OrGate",
                    "gates": [
                        {"type": "ConcreteGate", "allow": False},
                        {
                            "type": "AndGate",
                            "gates": [
                                {"type": "ConcreteGate", "allow": True},
                                {"type": "ConcreteGate", "allow": False}
                            ]
                        }
                    ]
                }
            ],
            "fail_closed": False
        }
        config = ConcreteGatingConfiguration.from_json(json_data)
        entity = {"some_property": "value"}
        assert config.check(entity) is False

    def test_complex_configuration_with_various_gate_combinations(self):
        PyGating.init()
        PyGating.register_gate(ConcreteGate)
        json_data = {
            "gates": [
                {
                    "type": "OrGate",
                    "gates": [
                        {"type": "ConcreteGate", "allow": False},
                        {"type": "AndGate", "gates": [{"type": "ConcreteGate", "allow": True}]}
                    ]
                },
                {"type": "ConcreteGate", "allow": True}
            ],
            "fail_closed": True
        }
        config = ConcreteGatingConfiguration.from_json(json_data)
        entity = {"some_property": "value"}
        assert config.check(entity) is True

    def test_fail_open_on_exception(self):
        class ExceptionThrowingGate(AbstractGate):
            def _check_gate(self, entity: Optional[Any] = None) -> bool:
                raise Exception("Simulated exception in gate check")

            @classmethod
            def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
                return super()._parse_json_params(gate_json)
        
        PyGating.init()
        PyGating.register_gate(ConcreteGate)
        PyGating.register_gate(ExceptionThrowingGate)
        json_data = {
            "gates": [
                {
                    "type": "OrGate",
                    "gates": [
                        {"type": "ExceptionThrowingGate", "allow": True}
                    ]
                }
            ],
            "fail_closed": False
        }
        config = ConcreteGatingConfiguration.from_json(json_data)
        entity = {"some_property": "value"}
        # Assuming the presence of an invalid gate type will raise an exception
        assert config.check(entity) is True

    def test_fail_closed_on_exception(self):
        class ExceptionThrowingGate(AbstractGate):
            def _check_gate(self, entity: Optional[Any] = None) -> bool:
                raise Exception("Simulated exception in gate check")

            @classmethod
            def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
                return super()._parse_json_params(gate_json)
        
        PyGating.init()
        PyGating.register_gate(ConcreteGate)
        PyGating.register_gate(ExceptionThrowingGate)
        json_data = {
            "gates": [
                {
                    "type": "OrGate",
                    "gates": [
                        {"type": "ExceptionThrowingGate", "allow": True}
                    ]
                }
            ],
            "fail_closed": True
        }
        config = ConcreteGatingConfiguration.from_json(json_data)
        entity = {"some_property": "value"}
        # Assuming the presence of an invalid gate type will raise an exception
        assert config.check(entity) is False

    def test_complex_configuration_with_entity_properties(self):
        PyGating.init()
        PyGating.register_gate(ConcreteGate)
        PyGating.register_gate(AgeGate)
        PyGating.register_gate(NameGate)
        json_data = {
            "gates": [
                {
                    "type": "AndGate",
                    "gates": [
                        {"type": "AgeGate", "min_age": 18, "entity_property": "age"},
                        {"type": "NameGate", "valid_names": ["Alice", "Bob"], "entity_property": "name"}
                    ]
                },
                {"type": "ConcreteGate", "allow": True}
            ],
            "fail_closed": True
        }
        config = ConcreteGatingConfiguration.from_json(json_data)

        young_entity = {"age": 17, "name": "Alice"}
        adult_entity = {"age": 20, "name": "Alice"}
        non_valid_name_entity = {"age": 25, "name": "Eve"}

        assert config.check(young_entity) is False  # Age fails
        assert config.check(adult_entity) is True   # Both age and name pass
        assert config.check(non_valid_name_entity) is False  # Name fails


    



