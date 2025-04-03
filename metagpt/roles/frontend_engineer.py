#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : frontend_engineer.py
"""

from typing import List, Optional, Set

from metagpt.actions import WriteFrontendCode
from metagpt.roles import Role
from metagpt.schema import Message

class FrontendEngineer(Role):
    """
    Role responsible for frontend development in startup projects.
    
    Attributes:
        name (str): The engineer's name
        profile (str): The role profile
        goal (str): The role's goal
        constraints (str): The role's constraints
    """
    
    name: str = "FrontendEngineer"
    profile: str = "Frontend Engineer"
    goal: str = "Create modern, responsive, and user-friendly frontend applications"
    constraints: str = (
        "The frontend should be built with modern frameworks, follow best practices, "
        "be responsive, accessible, and optimized for performance. Focus on user experience "
        "and maintainable code structure."
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_actions([WriteFrontendCode])
        self._watch([WriteFrontendCode])

    async def _act(self) -> Message | None:
        """Execute the frontend development process."""
        if self.rc.todo is None:
            return None
        return await self.rc.todo.run(self.rc.history) 