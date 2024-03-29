
from typing import Optional, Any, Dict
import pytest
from src.pygating.gates import PropertyGatingType
from src.pygating import GatingException

class ExamplePropertyGating(PropertyGatingType):
    def __init__(self, property_type: Optional[Any] = str, entity_property: Optional[str] = None, allow: bool = True):
        super().__init__(property_type=property_type, entity_property=entity_property, allow=allow)

    def _check_gate(self, entity: Optional[Any] = None) -> bool:
        return True
    
class TestPropertyGatingType:

    # Creating an instance of PropertyGatingType with valid parameters should not raise any exceptions.
    def test_valid_instance_creation(self):
        _ = ExamplePropertyGating=str()

    # Calling the entity_value method with a valid entity and no entity_property should return the entity.
    def test_entity_value_no_property_fixed(self):
        entity = "test_entity"
        gating_type = ExamplePropertyGating()

        result = gating_type.entity_value(entity)

        assert result == entity, "entity_value did not return the expected result"

    # Calling the entity_value method with a valid entity and an existing entity_property should return the value of the property.
    def test_entity_value_with_property(self):
        entity = type("TestEntity", (), {"property": "test_property"})()
        gating_type = ExamplePropertyGating(entity_property="property")

        result = gating_type.entity_value(entity)

        assert result == "test_property", "entity_value did not return the expected result"

    # Calling the entity_value method with an invalid entity should raise a GatingException.
    def test_invalid_entity_fixed(self):
        gating_type = ExamplePropertyGating()

        with pytest.raises(GatingException):
            _ = gating_type.entity_value(None)

    # Calling the entity_value method with a valid entity and an existing entity_property that throws an exception should raise a GatingException.
    def test_property_throws_exception_fixed(self):
        entity = type("TestEntity", (), {"property": lambda: 1/0})()
            
        gating_type = ExamplePropertyGating(entity_property="property")

        with pytest.raises(GatingException):
            _ = gating_type.entity_value(entity)

    def test_from_json_with_valid_data(self):
        json_data = {
            "property_type": str,
            "entity_property": "age",
            "allow": True
        }

        gate = ExamplePropertyGating.from_json(json_data)
        assert gate.property_type == str
        assert gate.entity_property == "age"

    def test_entity_without_required_property_raises_exception(self):
        gate = ExamplePropertyGating(entity_property="age")
        with pytest.raises(GatingException):
            gate.entity_value({"name": "John"})



    def test_entity_with_callable_property(self):
        class TestEntity:
            def __init__(self, age):
                self.age = age
            def get_age(self):
                return self.age
        gate = ExamplePropertyGating(property_type=int, entity_property="get_age")
        entity = TestEntity(25)
        result = gate.entity_value(entity)
        assert result == 25

