from typing import Any, Optional, List, Dict
from .property_gating_type import PropertyGatingType

class ListContainertGate(PropertyGatingType):
    def __init__(self, tag: Any, entity_property: Optional[str] = None, allow: bool = True):
        super().__init__(property_type=List, entity_property=entity_property, allow=allow)
        self.tag = tag

    def _check_gate(self, entity: Any) -> bool:
        entity_list = self.entity_value(entity)
        return self.tag in entity_list

    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        params = super()._parse_json_params(gate_json)
        
        if "tag" not in gate_json:
            raise ValueError("The 'tag' field must be provided")
        
        params["tag"] = gate_json["tag"]
        
        return params
