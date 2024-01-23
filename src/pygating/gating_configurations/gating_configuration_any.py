from ..pygating import AbstractGatingConfiguration
from typing import Any, Optional

class GatingConfigurationAny(AbstractGatingConfiguration):
    def _check_gating(self, entity: Optional[Any] = None):
        for gate in self.gates:
            if gate.check(entity):
                return True
            
        return False