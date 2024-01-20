from typing import Any,  Optional, Dict
from src.pygating.pygating import AbstractGate

class SimpleGate(AbstractGate):
    def _check_gate(self, entity: Optional[Any] = None) -> bool:
        return True
    