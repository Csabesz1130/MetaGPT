#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : data_privacy_officer.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.roles import Role
from metagpt.actions.ai_powered import WritePrivacyCode
from metagpt.schema import Message

class DataPrivacyOfficer(Role):
    """
    Role responsible for ensuring data privacy and compliance.
    
    Attributes:
        name (str): The role name
        profile (str): The role profile description
        goal (str): The role's main objective
        constraints (List[str]): The role's operational constraints
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.name = "DataPrivacyOfficer"
        self.profile = "Expert in data privacy and compliance"
        self.goal = "Ensure data privacy and regulatory compliance"
        self.constraints = [
            "Must comply with all relevant regulations",
            "Must implement proper data protection measures",
            "Must maintain audit trails",
            "Must ensure user privacy rights"
        ]
        
        self._init_actions([WritePrivacyCode])
        
    async def _act(self) -> Message:
        """
        Execute the privacy implementation process.
        
        Returns:
            Message: The result of the action
        """
        todo = self.get_memories(k=1)[0] if self.get_memories(k=1) else None
        
        if todo:
            # Execute the WritePrivacyCode action
            action = WritePrivacyCode()
            result = await action.run(messages=[todo])
            return result
        
        return Message(content="No task to process", role=self.name) 