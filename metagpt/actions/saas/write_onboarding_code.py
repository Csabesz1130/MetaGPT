#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : write_onboarding_code.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.actions import Action
from metagpt.schema import Message

class WriteOnboardingCode(Action):
    """
    Action for writing user onboarding code.
    
    Attributes:
        name (str): The action name
        context (str): The action context
    """
    
    name: str = "WriteOnboardingCode"
    context: str = "Write code for user onboarding"
    
    async def run(self, messages: List[Message]) -> Message:
        """
        Execute the onboarding code writing process.
        
        Args:
            messages (List[Message]): Previous messages
            
        Returns:
            Message: Generated code
        """
        prompt = """
        Write user onboarding code with the following features:
        
        1. Welcome Flow:
           - Personalized welcome messages
           - Account setup wizard
           - Feature discovery tour
        
        2. Feature Tutorials:
           - Interactive walkthroughs
           - Contextual tooltips
           - Video demonstrations
        
        3. Progress Tracking:
           - Onboarding checklist
           - Progress indicators
           - Achievement badges
        
        4. Contextual Help:
           - In-app documentation
           - Support chat integration
           - Knowledge base access
        
        The code should be:
        - User-friendly and intuitive
        - Customizable for different user segments
        - Responsive across devices
        - Easy to maintain and update
        """
        
        code = await self._aask(prompt)
        return Message(content=code, role="assistant") 