#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : devops_engineer.py
"""

from typing import List, Optional, Set

from metagpt.actions import SetupDevOps
from metagpt.roles import Role
from metagpt.schema import Message

class DevOpsEngineer(Role):
    """
    Role responsible for DevOps pipeline and infrastructure.
    
    Attributes:
        name (str): The engineer's name
        profile (str): The role profile
        goal (str): The role's goal
        constraints (str): The role's constraints
    """
    
    name: str = "DevOpsEngineer"
    profile: str = "DevOps Engineer"
    goal: str = "Set up robust DevOps pipeline and infrastructure for the startup"
    constraints: str = (
        "The DevOps setup should follow modern best practices, be automated, "
        "and support rapid development and deployment. Focus on CI/CD, containerization, "
        "and infrastructure as code."
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_actions([SetupDevOps])
        self._watch([SetupDevOps])

    async def _act(self) -> Message | None:
        """Execute the DevOps setup process."""
        if self.rc.todo is None:
            return None
        return await self.rc.todo.run(self.rc.history) 