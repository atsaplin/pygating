from datetime import datetime
from typing import Any, Dict, Optional

import dateutil.parser

from .property_gating_type import PropertyGatingType


class DateGate(PropertyGatingType):
    def __init__(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        entity_property: Optional[str] = None,
        allow: bool = True,
    ):
        super().__init__(
            property_type=datetime, entity_property=entity_property, allow=allow
        )
        self.start_date = start_date
        self.end_date = end_date

    def _check_gate(self, entity: Optional[Any] = None) -> bool:
        date_property = self._get_current_datetime()
        if entity:
            date_property = self.entity_value(entity)

        # If start_date is not defined, assume the gate is always open before end_date
        if self.start_date is None and self.end_date:
            return date_property <= self.end_date

        # If end_date is not defined, assume the gate is always open after start_date
        if self.end_date is None and self.start_date:
            return date_property >= self.start_date

        # If both dates are defined
        if self.start_date and self.end_date:
            return self.start_date <= date_property <= self.end_date

        # If neither date is defined, gate is always open
        return True

    def _get_current_datetime(self):
        return datetime.now()

    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        params = super()._parse_json_params(gate_json)
        start_date = gate_json.get("start_date")
        if start_date:
            if isinstance(start_date, str):
                start_date = dateutil.parser.parse(start_date)
            elif not isinstance(start_date, datetime):
                raise ValueError(f"'start_date' must be a datetime: {start_date}")

        end_date = gate_json.get("end_date")
        if end_date:
            if isinstance(end_date, str):
                end_date = dateutil.parser.parse(end_date)
            elif not isinstance(end_date, datetime):
                raise ValueError(f"'end_date' must be a datetime: {end_date}")

        if not start_date and not end_date:
            raise ValueError("Either 'start_date' or 'end_date' must be provided")

        params["start_date"] = start_date
        params["end_date"] = end_date

        return params
