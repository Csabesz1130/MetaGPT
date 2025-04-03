#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : write_frontend_code.py
"""

from typing import Dict, List, Optional

from metagpt.actions import Action
from metagpt.schema import Message

class WriteFrontendCode(Action):
    """
    Action for writing frontend code based on the architecture and requirements.
    """
    
    name: str = "WriteFrontendCode"
    
    async def run(self, context: List[Message] = None) -> Message:
        """Execute the frontend code generation process."""
        # Extract architecture and requirements from context
        architecture = ""
        requirements = ""
        
        if context:
            for msg in context:
                if "architecture" in msg.content.lower():
                    architecture = msg.content
                elif "requirements" in msg.content.lower():
                    requirements = msg.content
        
        # Create a detailed prompt for the LLM
        prompt = f"""
        Generate frontend code based on the following architecture and requirements:
        
        Architecture:
        {architecture}
        
        Requirements:
        {requirements}
        
        Consider the following aspects:
        1. Component Structure:
           - Create reusable components
           - Implement proper component hierarchy
           - Use modern state management
        
        2. User Interface:
           - Design responsive layouts
           - Implement modern UI patterns
           - Ensure accessibility
        
        3. Performance:
           - Optimize bundle size
           - Implement code splitting
           - Use proper caching strategies
        
        4. Testing:
           - Write unit tests for components
           - Implement integration tests
           - Add end-to-end tests
        
        Provide the code in a structured format with clear file organization.
        """
        
        # Call the LLM to generate the frontend code
        response = await self._aask(prompt)
        
        return Message(content=response) 