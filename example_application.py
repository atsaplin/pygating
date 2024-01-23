from src.pygating import PyGating
from src.pygating.gating_configurations import GatingConfigurationAll
from src.pygating.gates import PercentageGate, RandomGate
import random
import string

def generate_random_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))


class Name:
    def __init__(self, first, last):
        self._first = first
        self._last = last
        self.details = {"length": str(len(first + last))}

    @property
    def first(self):
        return self._first

    def last_name(self):
        return self._last

class Shop:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

class Entity:
    def __init__(self, id: str, shop):
        self.id = id
        self.shop = shop

    def get_id(self):
        return self.id

# Initialize PyGating
PyGating.init()

# Configure the gate
gate_config = GatingConfigurationAll(
    fail_closed=True,
    gates=[
        PercentageGate(percentage=10, allow=True, entity_property="shop.get_name.details.length"),
    ]
)

# gate_config = {
#     "type": "GatingConfigurationAll",
#     "fail_closed": True,
#     "gates": [
#         {
#             "type": "PercentageGate",
#             "percentage": 10.0,
#             "allow": True,
#             "entity_property": "id"
#         }
#     ]
# }

# Generate entities and check gate
num_entities = 1000
passed_count = 0

for _ in range(num_entities):
    first_name = random_string(random.randint(10, 20))
    last_name = random_string(random.randint(10, 20))
    name = Name(first=first_name, last=last_name)
    shop = Shop(name=name)
    entity = Entity(id=generate_random_id(), shop=shop)
    if PyGating.check_gating(gate_config, entity=entity):
        passed_count += 1
        
# Print out the percentage of entities that passed the gate
percentage_passed = (passed_count / num_entities) * 100
print(f"Percentage of entities that passed the gate: {percentage_passed}%") # Should be roughly 5%
