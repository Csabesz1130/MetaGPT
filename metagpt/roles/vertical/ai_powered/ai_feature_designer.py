#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : ai_feature_designer.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.roles import Role
from metagpt.actions.ai_powered import WriteAIFeatureCode
from metagpt.schema import Message

class AIFeatureDesigner(Role):
    """
    Role responsible for designing and implementing AI features.
    
    Attributes:
        name (str): The role name
        profile (str): The role profile description
        goal (str): The role's main objective
        constraints (List[str]): The role's operational constraints
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.name = "AIFeatureDesigner"
        self.profile = "Expert in designing and implementing AI features"
        self.goal = "Create effective AI features for applications"
        self.constraints = [
            "Must ensure model accuracy and reliability",
            "Must implement proper error handling",
            "Must optimize for performance",
            "Must follow AI ethics guidelines"
        ]
        
        self._init_actions([WriteAIFeatureCode])
        
    async def _act(self) -> Message:
        """
        Execute the AI feature design process.
        
        Returns:
            Message: The result of the action
        """
        todo = self.get_memories(k=1)[0] if self.get_memories(k=1) else None
        
        if todo:
            # Execute the WriteAIFeatureCode action
            action = WriteAIFeatureCode()
            result = await action.run(messages=[todo])
            return result
        
        return Message(content="No task to process", role=self.name) 