from abc import ABC, abstractmethod

# Define the Strategy Interface
class ActionStrategy(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        pass

# Concrete Strategy for Adding Requirement
class AddRequirementStrategy(ActionStrategy):
    def execute(self, requirement):
        print(f"Adding requirement: {requirement}")
