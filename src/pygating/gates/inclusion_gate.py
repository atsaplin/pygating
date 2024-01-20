from typing import Any,  Optional, List, Dict
from .property_gating_type import PropertyGatingType

class InclusionGate(PropertyGatingType):
    def __init__(self, valid_values: List[Any], entity_property: Optional[str] = None, allow: bool = True):
        super().__init__(property_type=None, entity_property=entity_property, allow=allow)
        self.valid_values = valid_values

    def _check_gate(self, entity: Any) -> bool:
        entity_value = self.entity_value(entity)
        return entity_value in self.valid_values
    
    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        params = super()._parse_json_params(gate_json)
        
        if "valid_values" not in gate_json or not isinstance(gate_json["valid_values"], list):
            raise ValueError("The 'valid_values' field must be provided and be a list")
        
        
        params["valid_values"] = gate_json["valid_values"]
        
        return params
    