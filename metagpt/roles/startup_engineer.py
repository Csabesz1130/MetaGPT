#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : startup_engineer.py
"""

from typing import List, Optional, Set

from metagpt.actions import WriteStartupCode
from metagpt.roles import Role
from metagpt.schema import Message

class StartupEngineer(Role):
    """
    A startup-specifikus kódgenerálásért felelős szerepkör.
    
    Attributes:
        name (str): A mérnök neve
        profile (str): A szerepkör profilja
        goal (str): A szerepkör célja
        constraints (str): A szerepkör korlátai
    """
    
    name: str = "StartupEngineer"
    profile: str = "Startup Engineer"
    goal: str = "Generate modern, scalable, and maintainable startup code"
    constraints: str = (
        "The code should follow modern best practices, be well-documented, "
        "and include proper testing. Focus on rapid development and MVP first, "
        "but ensure the code is scalable for future growth."
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_actions([WriteStartupCode])
        self._watch([WriteStartupCode])

    async def _act(self) -> Message | None:
        """Execute the startup code generation process."""
        if self.rc.todo is None:
            return None
        return await self.rc.todo.run(self.rc.history) 