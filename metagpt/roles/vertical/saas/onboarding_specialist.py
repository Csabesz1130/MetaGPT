#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : onboarding_specialist.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.actions import WriteOnboardingCode
from metagpt.roles import Role
from metagpt.schema import Message

class OnboardingSpecialist(Role):
    """
    Role responsible for user onboarding and activation in SaaS applications.
    
    Attributes:
        name (str): The specialist's name
        profile (str): The role profile
        goal (str): The role's goal
        constraints (str): The role's constraints
        onboarding_types (List[str]): Supported onboarding types
    """
    
    name: str = "OnboardingSpecialist"
    profile: str = "Onboarding Specialist"
    goal: str = "Create engaging and effective user onboarding experiences"
    constraints: str = (
        "The onboarding system should be intuitive, personalized, "
        "and help users achieve their first value quickly. "
        "Include progress tracking, contextual help, and feedback mechanisms."
    )
    
    onboarding_types: List[str] = [
        "guided_tour",
        "interactive_tutorial",
        "video_walkthrough",
        "checklist",
        "progressive_disclosure"
    ]
    
    def __init__(self, 
                 onboarding_type: str = "guided_tour",
                 **kwargs) -> None:
        """
        Initialize the OnboardingSpecialist role.
        
        Args:
            onboarding_type (str): The type of onboarding to implement
            **kwargs: Additional parameters for the parent class
        """
        super().__init__(**kwargs)
        self.onboarding_type = onboarding_type
        self.set_actions([WriteOnboardingCode])
        self._watch([WriteOnboardingCode])
        
    async def analyze_onboarding_requirements(self, requirements: str) -> Dict[str, str]:
        """
        Analyze requirements and determine optimal onboarding setup.
        
        Args:
            requirements (str): Project requirements
            
        Returns:
            Dict[str, str]: Recommended onboarding configuration
        """
        prompt = f"""
        Analyze the following SaaS requirements and recommend the most suitable onboarding setup:
        
        Requirements:
        {requirements}
        
        Consider the following aspects:
        1. Target user expertise level
        2. Application complexity
        3. Key features to highlight
        4. User engagement goals
        5. Support resources available
        
        Provide recommendations in the following format:
        {{
            "onboarding_type": "type_name",
            "steps": ["step1", "step2", "step3"],
            "engagement_features": ["feature1", "feature2"],
            "support_resources": ["resource1", "resource2"]
        }}
        """
        
        response = await self._aask(prompt)
        return eval(response)
        
    async def _act(self) -> Message | None:
        """
        Execute the onboarding implementation process.
        
        Returns:
            Message | None: Generated code or None
        """
        if self.rc.todo is None:
            return None
            
        # Analyze requirements if not already configured
        if not self.onboarding_type and self.rc.history:
            for msg in self.rc.history:
                if "requirements" in msg.content.lower():
                    config = await self.analyze_onboarding_requirements(msg.content)
                    self.onboarding_type = config["onboarding_type"]
                    break
                    
        # Generate onboarding code
        return await self.rc.todo.run(self.rc.history) 