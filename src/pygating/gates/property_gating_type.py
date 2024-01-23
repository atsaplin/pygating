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
            # Check for dictionary access
            if isinstance(entity, dict):
                if self.entity_property in entity:
                    value = entity[self.entity_property]
                else:
                    raise GatingException(f"Entity does not have a key named '{self.entity_property}'")
            elif hasattr(entity, self.entity_property):
                property = getattr(entity, self.entity_property)
                
                if callable(property):
                    if property.__code__.co_argcount:
                        try:
                            value = property()
                        except Exception as e:
                            raise GatingException(f"Entity function {self.entity_property} threw an exception, {e}")
                    else:
                        raise GatingException(f"Entity property {self.entity_property} is a function, which must not take paramaters")
                else:
                    value = property
            else:
                raise GatingException(f"Entity does not have a property or function named '{self.entity_property}'")
        

        if  self.property_type and not isinstance(value, self.property_type):
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