#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : write_customer_success_code.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.actions import Action
from metagpt.schema import Message

class WriteCustomerSuccessCode(Action):
    """
    Action for writing customer success code.
    
    Attributes:
        name (str): The action name
        context (str): The action context
    """
    
    name: str = "WriteCustomerSuccessCode"
    context: str = "Write code for customer success"
    
    async def run(self, messages: List[Message]) -> Message:
        """
        Execute the customer success code writing process.
        
        Args:
            messages (List[Message]): Previous messages
            
        Returns:
            Message: Generated code
        """
        prompt = """
        Write customer success code with the following features:
        
        1. Engagement Tracking:
           - User activity monitoring
           - Feature adoption metrics
           - Success milestone tracking
        
        2. Feedback Collection:
           - In-app surveys
           - NPS tracking
           - Feature request management
        
        3. Support Automation:
           - Chatbot integration
           - Knowledge base search
           - Ticket management
        
        4. Success Metrics:
           - Customer health scoring
           - Churn prediction
           - Expansion opportunities
        
        The code should be:
        - Proactive in identifying issues
        - Personalized for different segments
        - Integrated with support systems
        - Focused on user value delivery
        """
        
        code = await self._aask(prompt)
        return Message(content=code, role="assistant") 