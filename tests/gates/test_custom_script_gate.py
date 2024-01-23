from typing import Any,  Optional, Callable
from pygating.gates import CustomScriptGate
import pytest

class TestCustomScriptGate:

    # Can create an instance of CustomScriptGate with a script function and allow parameter
    def test_create_instance(self):
        script_function = lambda x: True
        gate = CustomScriptGate(script_function, allow=True)
        assert isinstance(gate, CustomScriptGate)
        assert gate.script_function == script_function
        assert gate.allow == True

    # Can call _check_gate method with an entity parameter and get a boolean value returned based on the script function
    def test__check_gate_with_entity(self):
        script_function = lambda x: True
        gate = CustomScriptGate(script_function, allow=True)
        entity = "test"
        assert gate._check_gate(entity) == True

    # Can call check method with an entity parameter and get a boolean value returned based on the script function and allow parameter
    def test_check_with_entity_and_allow(self):
        script_function = lambda x: True
        gate = CustomScriptGate(script_function, allow=True)
        entity = "test"
        assert gate.check(entity) == True

    # Script function returns True for None entity parameter
    def test_script_function_returns_true_for_none_entity(self):
        script_function = lambda x: True
        gate = CustomScriptGate(script_function, allow=True)
        assert gate._check_gate(None) == True

    # Script function returns False for None entity parameter
    def test_script_function_returns_false_for_none_entity(self):
        script_function = lambda x: False
        gate = CustomScriptGate(script_function, allow=True)
        assert gate._check_gate(None) == False

    # Script function raises an exception when called with an entity parameter
    def test_script_function_raises_exception_with_entity(self):
        script_function = lambda x: 1/0
        gate = CustomScriptGate(script_function, allow=True)
        with pytest.raises(Exception):
            gate._check_gate("test")