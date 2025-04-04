#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : write_subscription_code.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.actions import Action
from metagpt.schema import Message

class WriteSubscriptionCode(Action):
    """
    Action for writing subscription management code.
    
    Attributes:
        name (str): The action name
        context (str): The action context
    """
    
    name: str = "WriteSubscriptionCode"
    context: str = "Write code for subscription management"
    
    async def run(self, messages: List[Message]) -> Message:
        """
        Execute the subscription code writing process.
        
        Args:
            messages (List[Message]): Previous messages
            
        Returns:
            Message: Generated code
        """
        prompt = """
        Write subscription management code with the following features:
        
        1. Plan Management:
           - Create, update, and delete subscription plans
           - Handle plan upgrades and downgrades
           - Manage plan features and limits
        
        2. Payment Processing:
           - Handle payment methods
           - Process payments and refunds
           - Manage failed payments
        
        3. Invoice Generation:
           - Generate and send invoices
           - Handle tax calculations
           - Manage billing cycles
        
        4. Usage Tracking:
           - Track feature usage
           - Enforce usage limits
           - Generate usage reports
        
        The code should be:
        - Secure and compliant with PCI standards
        - Scalable for high transaction volumes
        - Easy to integrate with payment providers
        - Well-documented with clear error handling
        """
        
        code = await self._aask(prompt)
        return Message(content=code, role="assistant") 