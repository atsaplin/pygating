from typing import Any,  Optional, Callable, Dict
from ..pygating import AbstractGate

class CustomScriptGate(AbstractGate):
    def __init__(self, script_function: Callable[[Any], bool], allow: bool = True):
        super().__init__(allow=allow)
        self.script_function = script_function

    def _check_gate(self, entity: Optional[Any] = None) -> bool:
        return self.script_function(entity)
    
    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        raise NotImplementedError("CustomScriptGate cannot be instantiated from json")