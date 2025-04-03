#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : startup_architect.py
"""

from typing import List, Optional, Set

from metagpt.actions import WriteStartupArchitecture
from metagpt.roles import Role
from metagpt.schema import Message

class StartupArchitect(Role):
    """
    A startup architektúrájáért felelős szerepkör.
    
    Attributes:
        name (str): Az architekt neve
        profile (str): A szerepkör profilja
        goal (str): A szerepkör célja
        constraints (str): A szerepkör korlátai
    """
    
    name: str = "StartupArchitect"
    profile: str = "Startup Architect"
    goal: str = "Design scalable, maintainable, and modern startup architecture"
    constraints: str = (
        "The architecture should follow modern best practices, be cloud-native, "
        "and support rapid development and scaling. Consider microservices where appropriate, "
        "but don't over-engineer. Focus on MVP first."
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_actions([WriteStartupArchitecture])
        self._watch([WriteStartupArchitecture])

    async def _act(self) -> Message | None:
        """Execute the startup architecture design process."""
        if self.rc.todo is None:
            return None
        return await self.rc.todo.run(self.rc.history) 