#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : ai_powered_template.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.roles.vertical.ai_powered import (
    DataPipelineEngineer,
    MLOpsSpecialist,
    AIFeatureDesigner,
    DataPrivacyOfficer
)
from metagpt.schema import Message

class AI_Powered_Template:
    """
    Template for AI-powered applications.
    
    Attributes:
        data_source (str): The data source type
        deployment_platform (str): The deployment platform
        ai_capability (str): The AI capability type
        privacy_framework (str): The privacy framework
    """
    
    def __init__(self,
                 data_source: str = "database",
                 deployment_platform: str = "kubernetes",
                 ai_capability: str = "prediction",
                 privacy_framework: str = "gdpr") -> None:
        """
        Initialize the AI-powered application template.
        
        Args:
            data_source (str): The data source type
            deployment_platform (str): The deployment platform
            ai_capability (str): The AI capability type
            privacy_framework (str): The privacy framework
        """
        self.data_source = data_source
        self.deployment_platform = deployment_platform
        self.ai_capability = ai_capability
        self.privacy_framework = privacy_framework
        
        # Initialize roles
        self.data_pipeline_engineer = DataPipelineEngineer()
        self.mlops_specialist = MLOpsSpecialist()
        self.ai_feature_designer = AIFeatureDesigner()
        self.data_privacy_officer = DataPrivacyOfficer()
        
    async def analyze_requirements(self, requirements: str) -> Dict[str, str]:
        """
        Analyze project requirements and determine optimal configuration.
        
        Args:
            requirements (str): Project requirements
            
        Returns:
            Dict[str, str]: Recommended configuration
        """
        prompt = f"""
        Analyze the following AI application requirements and recommend the most suitable configuration:
        
        Requirements:
        {requirements}
        
        Consider the following aspects:
        1. Data handling needs
        2. Deployment requirements
        3. AI capabilities needed
        4. Privacy considerations
        
        Provide recommendations in the following format:
        {{
            "data_source": "source_type",
            "deployment_platform": "platform_name",
            "ai_capability": "capability_type",
            "privacy_framework": "framework_name"
        }}
        """
        
        # Get recommendations from each role
        data_pipeline_config = await self.data_pipeline_engineer._act()
        mlops_config = await self.mlops_specialist._act()
        ai_feature_config = await self.ai_feature_designer._act()
        privacy_config = await self.data_privacy_officer._act()
        
        # Combine and return recommendations
        return {
            "data_source": data_pipeline_config.content,
            "deployment_platform": mlops_config.content,
            "ai_capability": ai_feature_config.content,
            "privacy_framework": privacy_config.content
        }
        
    async def generate_code(self) -> Dict[str, Message]:
        """
        Generate code for each component of the AI application.
        
        Returns:
            Dict[str, Message]: Generated code for each component
        """
        return {
            "data_pipeline": await self.data_pipeline_engineer._act(),
            "mlops": await self.mlops_specialist._act(),
            "ai_features": await self.ai_feature_designer._act(),
            "privacy": await self.data_privacy_officer._act()
        }
        
    async def generate(self) -> Dict[str, Message]:
        """
        Generate the complete AI application.
        
        Returns:
            Dict[str, Message]: Generated application components
        """
        # Generate code for all components
        components = await self.generate_code()
        
        # Add any necessary integration code or configurations
        
        return components 