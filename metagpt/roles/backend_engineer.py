#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : backend_engineer.py
"""

from typing import List, Optional, Set

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
    """
    
    name: str = "BackendEngineer"
    profile: str = "Backend Engineer"
    goal: str = "Create robust, scalable, and secure backend services"
    constraints: str = (
        "The backend should be built with modern frameworks, follow best practices, "
        "be scalable, secure, and optimized for performance. Focus on API design, "
        "database optimization, and system architecture."
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_actions([WriteBackendCode])
        self._watch([WriteBackendCode])

    async def _act(self) -> Message | None:
        """Execute the backend development process."""
        if self.rc.todo is None:
            return None
        return await self.rc.todo.run(self.rc.history) 