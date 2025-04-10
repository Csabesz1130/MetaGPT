#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/4
@Author  : Gemini
@File    : budget.py
"""

from typing import Dict, Optional

class BudgetManager:
    """Manages spending limits for AI usage."""

    def __init__(self, budget_limit: float, costs_per_token: Dict[str, float], costs_per_call: Optional[Dict[str, float]] = None):
        """
        Initializes the BudgetManager.

        Args:
            budget_limit (float): The total budget limit.
            costs_per_token (Dict[str, float]): Dictionary mapping endpoint/model to cost per token.
            costs_per_call (Optional[Dict[str, float]]): Optional dictionary mapping endpoint/model to cost per API call.
        """
        if budget_limit <= 0:
            raise ValueError("Budget limit must be positive.")
        if not costs_per_token:
            raise ValueError("Costs per token must be provided.")
            
        self.budget_limit = budget_limit
        self.costs_per_token = costs_per_token
        self.costs_per_call = costs_per_call if costs_per_call else {}
        self.current_spending = 0.0

    def update_spending(self, endpoint: str, total_tokens: int, num_calls: int = 1):
        """Updates the current spending based on usage."""
        token_cost = self.costs_per_token.get(endpoint, 0) * total_tokens
        call_cost = self.costs_per_call.get(endpoint, 0) * num_calls
        self.current_spending += token_cost + call_cost

    def check_budget(self, potential_cost: float = 0.0) -> bool:
        """Checks if the current or potential spending is within the budget limit."""
        return (self.current_spending + potential_cost) <= self.budget_limit

    def get_remaining_budget(self) -> float:
        """Returns the remaining budget."""
        return max(0.0, self.budget_limit - self.current_spending)

    def get_current_spending(self) -> float:
        """Returns the current total spending."""
        return self.current_spending

    def is_budget_exceeded(self) -> bool:
        """Checks if the budget limit has been exceeded."""
        return self.current_spending > self.budget_limit
        
    def reset(self):
        """Resets the current spending to zero."""
        self.current_spending = 0.0 