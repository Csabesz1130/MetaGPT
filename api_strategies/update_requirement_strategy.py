from abc import ABC, abstractmethod

# Define the Strategy Interface (if not already defined)
class ActionStrategy(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        pass

# Concrete Strategy for Updating Requirement
class UpdateRequirementStrategy(ActionStrategy):
    def execute(self, requirement, new_version):
        print(f"Updating requirement {requirement} to version {new_version}")
