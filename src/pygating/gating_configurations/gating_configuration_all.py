from ..pygating import AbstractGatingConfiguration
from typing import Any, Optional

class GatingConfigurationAll(AbstractGatingConfiguration):
    def _check_gating(self, entity: Optional[Any] = None):
        for gate in self.gates:
            passed = gate.check(entity)

            if not passed:
                return False
            
        return True