#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : customer_success_agent.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.actions import WriteCustomerSuccessCode
from metagpt.roles import Role
from metagpt.schema import Message

class CustomerSuccessAgent(Role):
    """
    Role responsible for customer success and retention in SaaS applications.
    
    Attributes:
        name (str): The agent's name
        profile (str): The role profile
        goal (str): The role's goal
        constraints (str): The role's constraints
        retention_strategies (List[str]): Supported retention strategies
    """
    
    name: str = "CustomerSuccessAgent"
    profile: str = "Customer Success Agent"
    goal: str = "Implement customer success and retention features"
    constraints: str = (
        "The customer success system should be proactive, personalized, "
        "and focused on user value. Include engagement tracking, feedback loops, "
        "and automated support features."
    )
    
    retention_strategies: List[str] = [
        "proactive_engagement",
        "feedback_collection",
        "success_metrics",
        "support_automation",
        "community_building"
    ]
    
    def __init__(self, 
                 retention_strategy: str = "proactive_engagement",
                 **kwargs) -> None:
        """
        Initialize the CustomerSuccessAgent role.
        
        Args:
            retention_strategy (str): The retention strategy to implement
            **kwargs: Additional parameters for the parent class
        """
        super().__init__(**kwargs)
        self.retention_strategy = retention_strategy
        self.set_actions([WriteCustomerSuccessCode])
        self._watch([WriteCustomerSuccessCode])
        
    async def analyze_retention_requirements(self, requirements: str) -> Dict[str, str]:
        """
        Analyze requirements and determine optimal retention setup.
        
        Args:
            requirements (str): Project requirements
            
        Returns:
            Dict[str, str]: Recommended retention configuration
        """
        prompt = f"""
        Analyze the following SaaS requirements and recommend the most suitable retention setup:
        
        Requirements:
        {requirements}
        
        Consider the following aspects:
        1. Target customer segments
        2. Key success metrics
        3. Support channels
        4. Engagement opportunities
        5. Feedback mechanisms
        
        Provide recommendations in the following format:
        {{
            "retention_strategy": "strategy_name",
            "engagement_tactics": ["tactic1", "tactic2", "tactic3"],
            "success_metrics": ["metric1", "metric2"],
            "support_features": ["feature1", "feature2"]
        }}
        """
        
        response = await self._aask(prompt)
        return eval(response)
        
    async def _act(self) -> Message | None:
        """
        Execute the customer success implementation process.
        
        Returns:
            Message | None: Generated code or None
        """
        if self.rc.todo is None:
            return None
            
        # Analyze requirements if not already configured
        if not self.retention_strategy and self.rc.history:
            for msg in self.rc.history:
                if "requirements" in msg.content.lower():
                    config = await self.analyze_retention_requirements(msg.content)
                    self.retention_strategy = config["retention_strategy"]
                    break
                    
        # Generate customer success code
        return await self.rc.todo.run(self.rc.history) 