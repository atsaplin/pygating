from datetime import datetime
from typing import Any, Dict, Optional

from dateutil.parser import parse as parse_date

from .comparison_gate import ComparisonGate


class DateComparisonGate(ComparisonGate):
    def __init__(
        self,
        comparison_operator: str,
        comparison_value: datetime,
        entity_property: Optional[str] = None,
        allow: bool = True,
    ):
        super().__init__(
            comparison_operator=comparison_operator,
            comparison_value=comparison_value,
            property_type=datetime,
            entity_property=entity_property,
            allow=allow,
        )

    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        params = super()._parse_json_params(gate_json)

        comparison_value = gate_json.get("comparison_value")
        if comparison_value:
            if isinstance(comparison_value, str):
                comparison_value = parse_date(comparison_value)
            elif not isinstance(comparison_value, datetime):
                raise ValueError(
                    f"'comparison_value' must be a datetime: {comparison_value}"
                )
        else:
            raise ValueError("'comparison_value' must be provided")

        params["comparison_value"] = comparison_value

        return params
