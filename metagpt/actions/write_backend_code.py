#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : write_backend_code.py
"""

from typing import Dict, List, Optional

from metagpt.actions import Action
from metagpt.schema import Message

class WriteBackendCode(Action):
    """
    Action for writing backend code based on the architecture and requirements.
    """
    
    name: str = "WriteBackendCode"
    
    async def run(self, context: List[Message] = None) -> Message:
        """Execute the backend code generation process."""
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
        Generate backend code based on the following architecture and requirements:
        
        Architecture:
        {architecture}
        
        Requirements:
        {requirements}
        
        Consider the following aspects:
        1. API Design:
           - Create RESTful endpoints
           - Implement proper error handling
           - Use modern API patterns
        
        2. Database:
           - Design efficient database schema
           - Implement proper indexing
           - Use appropriate ORM
        
        3. Security:
           - Implement authentication
           - Add authorization
           - Follow security best practices
        
        4. Testing:
           - Write unit tests
           - Implement integration tests
           - Add API tests
        
        Provide the code in a structured format with clear file organization.
        """
        
        # Call the LLM to generate the backend code
        response = await self._aask(prompt)
        
        return Message(content=response) 