from typing import Any, Dict, Optional

from .comparison_gate import ComparisonGate


class NumericComparisonGate(ComparisonGate):
    def __init__(
        self,
        comparison_operator: str,
        comparison_value: float,
        entity_property: Optional[str] = None,
        allow: bool = True,
    ):
        super().__init__(
            comparison_operator=comparison_operator,
            comparison_value=comparison_value,
            property_type=(int, float),
            entity_property=entity_property,
            allow=allow,
        )

    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        params = super()._parse_json_params(gate_json)

        comparison_value = gate_json.get("comparison_value")
        if not comparison_value or not isinstance(comparison_value, (int, float)):
            raise ValueError(
                f"Comparison value must be an integer or float: {comparison_value}"
            )

        params["comparison_value"] = comparison_value

        return params
