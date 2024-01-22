from src.pygating import PyGating
from src.pygating.gating_configurations import GatingConfigurationAll
from src.pygating.gates import PercentageGate, RandomGate
import random
import string

def generate_random_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

class Entity:
    def __init__(self, id: str):
        self.id = id

# Initialize PyGating
PyGating.init()

# Configure the gate
gate_config = GatingConfigurationAll(
    fail_closed=True,
    gates=[
        PercentageGate(percentage=10, allow=True, entity_property="id"),
        RandomGate(chance=0.5)
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
    entity = Entity(id=generate_random_id())
    if PyGating.check_gating(gate_config, entity=entity):
        passed_count += 1

# Print out the percentage of entities that passed the gate
percentage_passed = (passed_count / num_entities) * 100
print(f"Percentage of entities that passed the gate: {percentage_passed}%") # Should be roughly 5%
