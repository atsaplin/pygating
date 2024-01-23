from typing import Any,  Optional, Dict
import random
from ..pygating import AbstractGate

class RandomGate(AbstractGate):
    def __init__(self, chance: float, allow: bool = True):
        super().__init__(allow=allow)
        if not 0 <= chance <= 1:
            raise ValueError("Chance must be between 0 and 1")
        self.chance = chance

    def _check_gate(self, entity: Optional[Any] = None) -> bool:
        if random.random() <= self.chance:
            return True
        
        return False
    
    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        params = super()._parse_json_params(gate_json)
        if "chance" not in gate_json or not isinstance(gate_json["chance"], (float, int)):
            raise ValueError("The 'chance' field must be a float or int")
        
        params["chance"] = gate_json["chance"]
        
        return params