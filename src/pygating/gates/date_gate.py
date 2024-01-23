from typing import Any,  Optional, Dict
from datetime import datetime
from ..pygating import AbstractGate
import dateutil.parser

class DateGate(AbstractGate):
    def __init__(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, allow: bool = True):
        super().__init__(allow=allow)
        self.start_date = start_date
        self.end_date = end_date

    def _check_gate(self, entity: Optional[Any] = None) -> bool:
        current_date = self._get_current_datetime()

        # If start_date is not defined, assume the gate is always open before end_date
        if self.start_date is None and self.end_date:
            return current_date <= self.end_date

        # If end_date is not defined, assume the gate is always open after start_date
        if self.end_date is None and self.start_date:
            return current_date >= self.start_date

        # If both dates are defined
        if self.start_date and self.end_date:
            return self.start_date <= current_date <= self.end_date

        # If neither date is defined, gate is always open
        return True
    
    def _get_current_datetime(self):
        return datetime.now()
    
    
    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        params = super()._parse_json_params(gate_json)
        start_date = dateutil.parser.parse(gate_json["start_date"]) if "start_date" in gate_json else None
        end_date = dateutil.parser.parse(gate_json["end_date"]) if "end_date" in gate_json else None
        
        params["start_date"] = start_date
        params["end_date"] = end_date
        
        return params