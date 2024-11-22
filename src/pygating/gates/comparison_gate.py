import operator
from typing import Any, Dict, Optional

from .property_gating_type import PropertyGatingType

COMPARISON_OPERATORS = {
    "eq": operator.eq,
    "lt": operator.lt,
    "le": operator.le,
    "gt": operator.gt,
    "ge": operator.ge,
    "ne": operator.ne,
}


class ComparisonGate(PropertyGatingType):
    def __init__(
        self,
        comparison_operator: str,
        comparison_value: Any,
        property_type: Any,
        entity_property: Optional[str] = None,
        allow: bool = True,
    ):
        if comparison_operator not in COMPARISON_OPERATORS:
            raise ValueError(
                f"Invalid comparison operator: {comparison_operator}. Must be one of {list(COMPARISON_OPERATORS.keys())}"
            )
        super().__init__(
            property_type=property_type, entity_property=entity_property, allow=allow
        )
        self.comparison_function = COMPARISON_OPERATORS[comparison_operator]
        self.comparison_value = comparison_value

    def _check_gate(self, entity: Optional[Any] = None) -> bool:
        value = self.entity_value(entity)
        return self.comparison_function(value, self.comparison_value)

    @classmethod
    def _parse_json_params(cls, gate_json: Dict[str, Any]) -> Dict:
        params = super()._parse_json_params(gate_json)

        comparison_operator = gate_json.get("comparison_operator")
        if not comparison_operator or comparison_operator not in COMPARISON_OPERATORS:
            raise ValueError(
                f"'comparison_operator' must be one of {list(COMPARISON_OPERATORS.keys())}: {comparison_operator}"
            )

        comparison_value = gate_json.get("comparison_value")
        if not comparison_value:
            raise ValueError("'comparison_value' must be provided")

        params["comparison_operator"] = comparison_operator
        params["comparison_value"] = comparison_value
        return params
