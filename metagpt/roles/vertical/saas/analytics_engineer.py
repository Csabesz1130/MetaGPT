#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : analytics_engineer.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.actions import WriteAnalyticsCode
from metagpt.roles import Role
from metagpt.schema import Message

class AnalyticsEngineer(Role):
    """
    Role responsible for analytics and metrics tracking in SaaS applications.
    
    Attributes:
        name (str): The engineer's name
        profile (str): The role profile
        goal (str): The role's goal
        constraints (str): The role's constraints
        metrics_types (List[str]): Supported metrics types
    """
    
    name: str = "AnalyticsEngineer"
    profile: str = "Analytics Engineer"
    goal: str = "Implement comprehensive analytics and metrics tracking"
    constraints: str = (
        "The analytics system should be scalable, real-time, "
        "and provide actionable insights. Include user behavior tracking, "
        "performance metrics, and business KPIs."
    )
    
    metrics_types: List[str] = [
        "user_engagement",
        "feature_usage",
        "performance",
        "business",
        "security"
    ]
    
    def __init__(self, 
                 metrics_type: str = "user_engagement",
                 **kwargs) -> None:
        """
        Initialize the AnalyticsEngineer role.
        
        Args:
            metrics_type (str): The type of metrics to implement
            **kwargs: Additional parameters for the parent class
        """
        super().__init__(**kwargs)
        self.metrics_type = metrics_type
        self.set_actions([WriteAnalyticsCode])
        self._watch([WriteAnalyticsCode])
        
    async def analyze_analytics_requirements(self, requirements: str) -> Dict[str, str]:
        """
        Analyze requirements and determine optimal analytics setup.
        
        Args:
            requirements (str): Project requirements
            
        Returns:
            Dict[str, str]: Recommended analytics configuration
        """
        prompt = f"""
        Analyze the following SaaS requirements and recommend the most suitable analytics setup:
        
        Requirements:
        {requirements}
        
        Consider the following aspects:
        1. Key business metrics
        2. User behavior patterns
        3. Performance indicators
        4. Security monitoring needs
        5. Reporting requirements
        
        Provide recommendations in the following format:
        {{
            "metrics_type": "type_name",
            "tracked_events": ["event1", "event2", "event3"],
            "dashboards": ["dashboard1", "dashboard2"],
            "alerts": ["alert1", "alert2"]
        }}
        """
        
        response = await self._aask(prompt)
        return eval(response)
        
    async def _act(self) -> Message | None:
        """
        Execute the analytics implementation process.
        
        Returns:
            Message | None: Generated code or None
        """
        if self.rc.todo is None:
            return None
            
        # Analyze requirements if not already configured
        if not self.metrics_type and self.rc.history:
            for msg in self.rc.history:
                if "requirements" in msg.content.lower():
                    config = await self.analyze_analytics_requirements(msg.content)
                    self.metrics_type = config["metrics_type"]
                    break
                    
        # Generate analytics code
        return await self.rc.todo.run(self.rc.history) 