class CoreEngine:
    def __init__(self):
        self.action_registry = {}  # Map action names to strategy classes

    def register_action(self, action_name, strategy_class):
        self.action_registry[action_name] = strategy_class

    def execute_action(self, action_name, **kwargs):
        strategy_class = self.action_registry.get(action_name)
        if not strategy_class:
            raise ValueError(f"Unknown action: {action_name}")
        strategy = strategy_class()
        strategy.execute(**kwargs)
