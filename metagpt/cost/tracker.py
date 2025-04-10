#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/4
@Author  : Gemini
@File    : tracker.py
"""

import time
from collections import defaultdict

class UsageTracker:
    """Tracks API calls and token usage for cost management."""

    def __init__(self):
        self.api_calls = defaultdict(int)
        self.token_usage = defaultdict(lambda: {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0})
        self.timestamps = defaultdict(list)

    def log_api_call(self, endpoint: str):
        """Logs an API call to a specific endpoint."""
        self.api_calls[endpoint] += 1
        self.timestamps[endpoint].append(time.time())

    def log_token_usage(self, endpoint: str, prompt_tokens: int, completion_tokens: int):
        """Logs token usage for a specific endpoint."""
        self.token_usage[endpoint]['prompt_tokens'] += prompt_tokens
        self.token_usage[endpoint]['completion_tokens'] += completion_tokens
        self.token_usage[endpoint]['total_tokens'] += prompt_tokens + completion_tokens
        self.log_api_call(endpoint) # Assume token usage logging implies an API call

    def get_usage_summary(self) -> dict:
        """Returns a summary of API calls and token usage."""
        return {
            'api_calls': dict(self.api_calls),
            'token_usage': dict(self.token_usage)
        }

    def get_usage_for_endpoint(self, endpoint: str) -> dict:
        """Returns usage data for a specific endpoint."""
        return {
            'calls': self.api_calls.get(endpoint, 0),
            'prompt_tokens': self.token_usage[endpoint]['prompt_tokens'],
            'completion_tokens': self.token_usage[endpoint]['completion_tokens'],
            'total_tokens': self.token_usage[endpoint]['total_tokens'],
            'timestamps': self.timestamps.get(endpoint, [])
        }

    def reset(self):
        """Resets all tracked usage data."""
        self.api_calls.clear()
        self.token_usage.clear()
        self.timestamps.clear() 