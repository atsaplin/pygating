from typing import Any,  Optional, Dict
from .property_gating_type import PropertyGatingType
import re

class RegexGate(PropertyGatingType):
    def __init__(self, pattern: str, entity_property: Optional[str] = None, allow: bool = True):
        super().__init__(property_type=str, entity_property=entity_property, allow=allow)

        self.pattern = pattern

    def _check_gate(self, entity: Any) -> bool:
        return bool(re.match(self.pattern, self.entity_value(entity)))
    
    
    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        params = super()._parse_json_params(gate_json)

        if "pattern" not in gate_json or not isinstance(gate_json["pattern"], str):
            raise ValueError("The 'entity_property' field must be provided and be a str")
        

        params["pattern"] = gate_json["pattern"]

        return params
    