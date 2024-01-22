# PyGating

PyGating is a small but simple python library that enables you to quickly introduce a/b testing, control code flow, and introduce control switches to your codebase that can be controlled via both code and json-based configs.

PyGating supports entity-based checks, allowing you to define in the gating configuration exactly the properties, functions, and/or keys the gate will check based on a entity you will pass in at check time.

Check out the respository [here](https://github.com/atsaplin/pygating) for more information and documentation

## Features

- **Extensible Framework**: Create custom gates by extending base gate classes.
- **Entity-based gates**: Define gate configurations based on entity properties/functions to make gates dynamic
- **Consistant Hashing**: Entity-based gate checks will pass/fail consistently based on property hashing
- **JSON Configuration**: Supports gate configuration defined in json so that you can pull gates configs from databases
- **Predefined Gates**: Includes `DateGate`, `PercentageGate`, `RandomGate`, `InclusionGate`, and more.
- **Custom Gate Configurations**: Combine gates to create complex gating logic.

## Quick Usage Example
This example will only permit 10% of entities/code invocations to continue.

We can use either a RandomGate for pure 10% random chance or a PercentageGate for a consistant result based on the passed entity

- Initialize Pygating Library and imports
```python
from pygating import PyGating
from pygating.gating_configurations import GatingConfigurationAll
from pygating.gates import PercentageGate

PyGating.init() # only needs to be done once in the application
```
- Define a gate config (code or json):

Code-based config
```python
gate_config = GatingConfigurationAll(
    fail_closed=True, #if an exception is thrown, the gate check returns False
    gates=[
        PercentageGate(percentage=10, allow=True, entity_property="id") # 10% of entities passed into the gate check will pass based on their id field 
    ]
)
```
##### or
Json-based config
```json
gate_config = {
    "type": "GatingConfigurationAll",
    "fail_closed": True,
    "gates": [
        {
            "type": "PercentageGate",
            "percentage": 10.0,
            "allow": True,
            "entity_property": "id"
        }
    ]
}
```
- Use gate in your code:
```python
class Entity:
    def __init__(self, id: str):
        self.id = id

example_entity = Entity(id="dfa2oi1nrffvnoivwe")

if PyGating.check_gating(gate_config, entity=entity):
    print("Gate passed!") # Will pass for 10% of entity ids, and will be consistent for the same ids
else:
    print("Gate Failed")
```

## Installation
```bash
pip install pygating
```
