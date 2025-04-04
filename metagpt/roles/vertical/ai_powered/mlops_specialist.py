#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : mlops_specialist.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.roles import Role
from metagpt.actions.ai_powered import WriteMLOpsCode
from metagpt.schema import Message

class MLOpsSpecialist(Role):
    """
    Role responsible for MLOps implementation and management.
    
    Attributes:
        name (str): The role name
        profile (str): The role profile description
        goal (str): The role's main objective
        constraints (List[str]): The role's operational constraints
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.name = "MLOpsSpecialist"
        self.profile = "Expert in implementing and managing MLOps infrastructure"
        self.goal = "Create robust MLOps infrastructure for AI applications"
        self.constraints = [
            "Must ensure model reproducibility",
            "Must implement proper monitoring and alerting",
            "Must follow security best practices",
            "Must optimize for scalability and reliability"
        ]
        
        self._init_actions([WriteMLOpsCode])
        
    async def _act(self) -> Message:
        """
        Execute the MLOps implementation process.
        
        Returns:
            Message: The result of the action
        """
        todo = self.get_memories(k=1)[0] if self.get_memories(k=1) else None
        
        if todo:
            # Execute the WriteMLOpsCode action
            action = WriteMLOpsCode()
            result = await action.run(messages=[todo])
            return result
        
        return Message(content="No task to process", role=self.name) 