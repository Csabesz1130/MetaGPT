#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/4
@Author  : Gemini
@File    : optimizer.py
"""

from typing import Dict, List, Any
from metagpt.cost.tracker import UsageTracker # Assuming UsageTracker is in this path

class CostOptimizer:
    """Suggests efficiency improvements for AI usage based on tracked data."""

    def __init__(self, model_costs: Dict[str, float], cheaper_model_map: Dict[str, str], 
                 high_usage_threshold: int = 10000, frequent_call_threshold: int = 100):
        """
        Initializes the CostOptimizer.

        Args:
            model_costs (Dict[str, float]): Costs per token for different models/endpoints.
            cheaper_model_map (Dict[str, str]): Mapping from expensive models to cheaper alternatives.
            high_usage_threshold (int): Token threshold to flag an endpoint as high usage.
            frequent_call_threshold (int): Call count threshold to flag an endpoint as frequently called.
        """
        self.model_costs = model_costs
        self.cheaper_model_map = cheaper_model_map
        self.high_usage_threshold = high_usage_threshold
        self.frequent_call_threshold = frequent_call_threshold

    def analyze_usage(self, tracker: UsageTracker) -> List[Dict[str, Any]]:
        """Analyzes usage data from a UsageTracker and provides optimization suggestions."""
        suggestions = []
        usage_summary = tracker.get_usage_summary()

        for endpoint, usage in usage_summary['token_usage'].items():
            total_tokens = usage['total_tokens']
            num_calls = usage_summary['api_calls'].get(endpoint, 0)
            current_cost_per_token = self.model_costs.get(endpoint)

            # Suggest cheaper model if available and cost is known
            if current_cost_per_token and endpoint in self.cheaper_model_map:
                cheaper_model = self.cheaper_model_map[endpoint]
                cheaper_cost_per_token = self.model_costs.get(cheaper_model)
                if cheaper_cost_per_token and cheaper_cost_per_token < current_cost_per_token:
                    potential_savings = (current_cost_per_token - cheaper_cost_per_token) * total_tokens
                    suggestions.append({
                        'type': 'model_change',
                        'endpoint': endpoint,
                        'suggestion': f"Consider switching from '{endpoint}' to the cheaper model '{cheaper_model}'.",
                        'potential_savings': round(potential_savings, 4),
                        'current_model': endpoint,
                        'suggested_model': cheaper_model
                    })

            # Suggest prompt optimization for high token usage
            if total_tokens > self.high_usage_threshold:
                avg_tokens_per_call = total_tokens / num_calls if num_calls > 0 else 0
                suggestions.append({
                    'type': 'prompt_optimization',
                    'endpoint': endpoint,
                    'suggestion': f"Endpoint '{endpoint}' has high token usage ({total_tokens} tokens). Consider optimizing prompts to reduce token count.",
                    'total_tokens': total_tokens,
                    'average_tokens_per_call': round(avg_tokens_per_call, 2)
                })

            # Suggest caching for frequently called endpoints
            if num_calls > self.frequent_call_threshold:
                suggestions.append({
                    'type': 'caching',
                    'endpoint': endpoint,
                    'suggestion': f"Endpoint '{endpoint}' is called frequently ({num_calls} times). Consider implementing caching to reduce calls.",
                    'call_count': num_calls
                })
                
        # Add more complex analyses if needed, e.g., identifying redundant calls, batching opportunities

        return suggestions 