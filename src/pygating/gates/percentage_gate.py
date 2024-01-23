from typing import Any,  Optional, Dict
from .property_gating_type import PropertyGatingType
import hashlib

class PercentageGate(PropertyGatingType):
    def __init__(self, percentage: float, entity_property: Optional[str] = None, salt: Optional[str] = None, allow: bool = True):
        super().__init__(property_type=str, entity_property=entity_property, allow=allow)
        self.salt = salt

        if not (0 <= percentage <= 100):
            raise ValueError("Percentage must be between 0 and 100")
                             
        self.percentage = percentage


    def _check_gate(self, entity: Any) -> bool:
        property_value = self.entity_value(entity)

        if self.salt:
            property_value += self.salt

        # Convert the property value to a string and hash it
        hash_value = int(hashlib.md5(str(property_value).encode()).hexdigest(), 16)
        user_percentage = (hash_value % 10000) / 100.0  # Maps the hash to a value between 0.00-99.99

        return user_percentage < self.percentage
    
    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        params = super()._parse_json_params(gate_json)

        if "percentage" not in gate_json or not isinstance(gate_json["percentage"], (float, int)):
            raise ValueError("The 'percentage' field must be provided and be a float or an int")
        
        if "salt" in gate_json:
            if not isinstance(gate_json["salt"], str):
                raise ValueError("The 'salt' field must be a str")
            params["salt"] = gate_json["salt"]

        params["percentage"] = gate_json["percentage"]

        return params
    