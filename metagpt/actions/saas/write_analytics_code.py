#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : write_analytics_code.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.actions import Action
from metagpt.schema import Message

class WriteAnalyticsCode(Action):
    """
    Action for writing analytics tracking code.
    
    Attributes:
        name (str): The action name
        context (str): The action context
    """
    
    name: str = "WriteAnalyticsCode"
    context: str = "Write code for analytics tracking"
    
    async def run(self, messages: List[Message]) -> Message:
        """
        Execute the analytics code writing process.
        
        Args:
            messages (List[Message]): Previous messages
            
        Returns:
            Message: Generated code
        """
        prompt = """
        Write analytics tracking code with the following features:
        
        1. Event Tracking:
           - User actions and behaviors
           - Feature usage patterns
           - Error and exception tracking
        
        2. Dashboard Creation:
           - Real-time metrics display
           - Custom report generation
           - Data visualization tools
        
        3. Report Generation:
           - Scheduled reports
           - Export functionality
           - Report templates
        
        4. Alert System:
           - Threshold monitoring
           - Notification rules
           - Escalation procedures
        
        The code should be:
        - Privacy-compliant (GDPR, CCPA)
        - Performant with minimal overhead
        - Scalable for high data volumes
        - Easy to integrate with analytics providers
        """
        
        code = await self._aask(prompt)
        return Message(content=code, role="assistant") 