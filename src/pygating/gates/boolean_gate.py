from typing import Any,  Optional, Dict
from .property_gating_type import PropertyGatingType

class BooleanGate(PropertyGatingType):
    def __init__(self, entity_property: Optional[str] = None, allow: bool = True):
        super().__init__(property_type=bool, entity_property=entity_property, allow=allow)


    def _check_gate(self, entity: Any) -> bool:
        return self.entity_value(entity)
    
    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        params = super()._parse_json_params(gate_json)
        
        return params
    