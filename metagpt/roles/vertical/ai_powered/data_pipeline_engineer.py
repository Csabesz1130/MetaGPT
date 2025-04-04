#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : data_pipeline_engineer.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.roles import Role
from metagpt.actions.ai_powered import WriteDataPipelineCode
from metagpt.schema import Message

class DataPipelineEngineer(Role):
    """
    Role responsible for designing and implementing data pipelines.
    
    Attributes:
        name (str): The role name
        profile (str): The role profile description
        goal (str): The role's main objective
        constraints (List[str]): The role's operational constraints
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.name = "DataPipelineEngineer"
        self.profile = "Expert in designing and implementing scalable data pipelines"
        self.goal = "Create efficient and reliable data pipelines for AI applications"
        self.constraints = [
            "Must ensure data quality and integrity",
            "Must implement proper error handling and monitoring",
            "Must follow data privacy and security best practices",
            "Must optimize for performance and scalability"
        ]
        
        self._init_actions([WriteDataPipelineCode])
        
    async def _act(self) -> Message:
        """
        Execute the data pipeline engineering process.
        
        Returns:
            Message: The result of the action
        """
        todo = self.get_memories(k=1)[0] if self.get_memories(k=1) else None
        
        if todo:
            # Execute the WriteDataPipelineCode action
            action = WriteDataPipelineCode()
            result = await action.run(messages=[todo])
            return result
        
        return Message(content="No task to process", role=self.name) 