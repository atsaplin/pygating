from typing import Any,  Optional, Dict
from ..pygating import AbstractGate, GatingException

class PropertyGatingType(AbstractGate):
    def __init__(self, property_type: Any, entity_property: Optional[str] = None, allow: bool = True):
        super().__init__(allow=allow)
        self.property_type = property_type
        self.entity_property = entity_property

    def entity_value(self, entity: Any) -> Any:
        if not entity:
            raise GatingException(f"Entity must be provided when using gate of type: {self.__class__.__name__}")

        value = entity
        if self.entity_property:
            properties = self.entity_property.split('.')
            for prop in properties:
                if isinstance(value, dict):
                    if prop in value:
                        value = value[prop]
                    else:
                        raise GatingException(f"Entity does not have a key named '{prop}'")
                elif hasattr(value, prop):
                    value = getattr(value, prop)
                    if callable(value):
                        try:
                            value = value()
                        except Exception as e:
                            raise GatingException(f"Entity function {prop} threw an exception, {e}")
                else:
                    raise GatingException(f"Entity does not have a property or function named '{prop}'")

        if self.property_type and not isinstance(value, self.property_type):
            raise GatingException(f"Entity is not or does not return expected type of: {self.property_type.__name__}")

        return value
    
    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        params = super()._parse_json_params(gate_json)
        if "entity_property" in gate_json:
            if  not isinstance(gate_json["entity_property"], str):
                raise ValueError("The 'gates' field must be a str")
        
            params["entity_property"] = gate_json.get("entity_property", None)

        return params