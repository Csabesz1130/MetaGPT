from core_engine import CoreEngine
from api_strategies.add_requirement_strategy import AddRequirementStrategy
from api_strategies.update_requirement_strategy import UpdateRequirementStrategy

# Instantiate CoreEngine and Register Strategies
engine = CoreEngine()
engine.register_action('add_requirement', AddRequirementStrategy)
engine.register_action('update_requirement', UpdateRequirementStrategy)

# Test the setup
engine.execute_action('add_requirement', requirement='numpy')
engine.execute_action('update_requirement', requirement='numpy', new_version='1.21.0')
