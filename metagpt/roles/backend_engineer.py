#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : backend_engineer.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.actions import WriteBackendCode
from metagpt.roles import Role
from metagpt.schema import Message

class BackendEngineer(Role):
    """
    Role responsible for backend development in startup projects.
    
    Attributes:
        name (str): The engineer's name
        profile (str): The role profile
        goal (str): The role's goal
        constraints (str): The role's constraints
        tech_stack (Dict[str, str]): The technology stack and versions
        knowledge_base (Dict[str, str]): Tech stack specific knowledge base
    """
    
    name: str = "BackendEngineer"
    profile: str = "Backend Engineer"
    goal: str = "Create robust, scalable, and secure backend services"
    constraints: str = (
        "The backend should be built with modern frameworks, follow best practices, "
        "be scalable, secure, and optimized for performance. Focus on API design, "
        "database optimization, and system architecture."
    )
    
    def __init__(self, tech_stack: Optional[Dict[str, str]] = None, **kwargs) -> None:
        """
        Initialize the BackendEngineer role.
        
        Args:
            tech_stack (Dict[str, str], optional): The technology stack to use.
                Example: {"framework": "fastapi@0.104.0", "database": "postgresql@15.0"}
            **kwargs: Additional parameters for the parent class
        """
        super().__init__(**kwargs)
        self.tech_stack = tech_stack or {}
        self.knowledge_base = {}
        self.set_actions([WriteBackendCode])
        self._watch([WriteBackendCode])
        
    async def analyze_tech_requirements(self, requirements: str) -> Dict[str, str]:
        """
        Analyze requirements and determine optimal technology choices.
        
        Args:
            requirements (str): Project requirements
            
        Returns:
            Dict[str, str]: Recommended technologies and versions
        """
        prompt = f"""
        Analyze the following backend requirements and recommend the most suitable technology stack:
        
        Requirements:
        {requirements}
        
        Consider the following aspects:
        1. API requirements (REST, GraphQL, etc.)
        2. Database needs (SQL, NoSQL, etc.)
        3. Authentication requirements
        4. Scalability needs
        5. Performance requirements
        
        Provide recommendations in the following format:
        {{
            "framework": "framework@version",
            "database": "database@version",
            "orm": "orm@version",
            "auth": "auth@version",
            "cache": "cache@version"
        }}
        """
        
        response = await self._aask(prompt)
        return eval(response)  # Safe as response format is known
        
    def load_tech_stack_knowledge(self, tech: str) -> None:
        """
        Load tech stack specific knowledge base.
        
        Args:
            tech (str): Technology name (e.g., "fastapi", "postgresql")
        """
        knowledge_path = Path(__file__).parent / "knowledge" / f"{tech}_knowledge.txt"
        if knowledge_path.exists():
            with open(knowledge_path, "r", encoding="utf-8") as f:
                self.knowledge_base[tech] = f.read()
                
    async def _act(self) -> Message | None:
        """
        Execute the backend development process.
        
        Returns:
            Message | None: Generated code or None
        """
        if self.rc.todo is None:
            return None
            
        # Tech stack analysis and loading
        if not self.tech_stack and self.rc.history:
            for msg in self.rc.history:
                if "requirements" in msg.content.lower():
                    self.tech_stack = await self.analyze_tech_requirements(msg.content)
                    break
                    
        # Load knowledge base
        for tech in self.tech_stack.keys():
            self.load_tech_stack_knowledge(tech)
            
        # Generate code with tech stack consideration
        return await self.rc.todo.run(self.rc.history) 