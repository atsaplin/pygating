from typing import Any,  Optional, List, Dict
from ..pygating import AbstractGate, GatingException


class AndGate(AbstractGate):
    def __init__(self, gates: List[AbstractGate], allow: bool = True):
        super().__init__(allow=allow)
        if not gates:
            raise GatingException("The 'gates' list cannot be empty.")
        for gate in gates:
            if not isinstance(gate, AbstractGate):
                raise GatingException("All elements in 'gates' must be instances of 'AbstractGate'")
            
        self.gates = gates

    def _check_gate(self, entity: Optional[Any] = None) -> bool:
        return all(gate.check(entity) for gate in self.gates)
    
    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        params = super()._parse_json_params(gate_json)

        if "gates" not in gate_json or not isinstance(gate_json["gates"], list):
            raise ValueError("The 'gates' field must be provided and be a list")
        
        gates = []
        for gate_obj in gate_json["gates"]:
            gate_name = gate_obj["type"]
            gates.append(cls.get_gate_type_from_name(gate_name).from_json(gate_obj))

        params["gates"] = gates
        
        return params