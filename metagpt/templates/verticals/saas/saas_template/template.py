#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : template.py
"""

import asyncio
import os
from pathlib import Path
from typing import Dict, List, Optional, Set

from metagpt.roles.vertical.saas import (
    SubscriptionManager,
    OnboardingSpecialist,
    AnalyticsEngineer,
    CustomerSuccessAgent
)

class SAAS_Template:
    """
    Template for SaaS application development.
    
    Attributes:
        name (str): The template name
        description (str): Template description
        roles (List[Role]): Required roles
        components (Dict[str, str]): Core components
    """
    
    name: str = "SAAS_Template"
    description: str = "Template for building SaaS applications"
    
    def __init__(self,
                 billing_model: str = "subscription",
                 onboarding_type: str = "guided_tour",
                 metrics_type: str = "user_engagement",
                 retention_strategy: str = "proactive_engagement") -> None:
        """
        Initialize the SaaS template.
        
        Args:
            billing_model (str): The billing model to use
            onboarding_type (str): The onboarding type to implement
            metrics_type (str): The metrics type to track
            retention_strategy (str): The retention strategy to employ
        """
        self.roles = [
            SubscriptionManager(billing_model=billing_model),
            OnboardingSpecialist(onboarding_type=onboarding_type),
            AnalyticsEngineer(metrics_type=metrics_type),
            CustomerSuccessAgent(retention_strategy=retention_strategy)
        ]
        
        self.components = {
            "subscription_management": {
                "description": "Handle billing, plans, and payments",
                "features": [
                    "plan_management",
                    "payment_processing",
                    "invoice_generation",
                    "usage_tracking"
                ]
            },
            "user_onboarding": {
                "description": "Guide users through initial setup",
                "features": [
                    "welcome_flow",
                    "feature_tutorials",
                    "progress_tracking",
                    "contextual_help"
                ]
            },
            "analytics": {
                "description": "Track and analyze user behavior",
                "features": [
                    "event_tracking",
                    "dashboard_creation",
                    "report_generation",
                    "alert_system"
                ]
            },
            "customer_success": {
                "description": "Support user retention and growth",
                "features": [
                    "engagement_tracking",
                    "feedback_collection",
                    "support_automation",
                    "success_metrics"
                ]
            }
        }
        
    def get_directory_structure(self) -> Dict[str, List[str]]:
        """
        Get the recommended directory structure.
        
        Returns:
            Dict[str, List[str]]: Directory structure
        """
        return {
            "src": [
                "subscription",
                "onboarding",
                "analytics",
                "customer_success"
            ],
            "tests": [
                "subscription",
                "onboarding",
                "analytics",
                "customer_success"
            ],
            "docs": [
                "api",
                "user_guides",
                "developer_guides"
            ],
            "config": [
                "billing",
                "onboarding",
                "analytics",
                "retention"
            ]
        }
        
    def get_required_dependencies(self) -> Dict[str, str]:
        """
        Get the required dependencies.
        
        Returns:
            Dict[str, str]: Dependencies with versions
        """
        return {
            "stripe": ">=7.0.0",
            "mixpanel": ">=4.0.0",
            "segment": ">=2.0.0",
            "intercom": ">=3.0.0",
            "sentry": ">=1.0.0"
        }
        
    def get_configuration_options(self) -> Dict[str, Dict[str, str]]:
        """
        Get the configuration options.
        
        Returns:
            Dict[str, Dict[str, str]]: Configuration options
        """
        return {
            "billing": {
                "provider": "stripe",
                "currency": "USD",
                "tax_inclusive": "true"
            },
            "onboarding": {
                "type": "guided_tour",
                "skip_option": "true",
                "progress_save": "true"
            },
            "analytics": {
                "provider": "mixpanel",
                "tracking_enabled": "true",
                "privacy_mode": "true"
            },
            "retention": {
                "strategy": "proactive_engagement",
                "automation_enabled": "true",
                "feedback_enabled": "true"
            }
        }
        
    async def generate(self, output_dir: str = ".") -> None:
        """
        Generate the SaaS application template.
        
        Args:
            output_dir (str): Output directory for generated code
        """
        # Create directory structure
        for dir_name, subdirs in self.get_directory_structure().items():
            dir_path = Path(output_dir) / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            
            for subdir in subdirs:
                subdir_path = dir_path / subdir
                subdir_path.mkdir(parents=True, exist_ok=True)
                
        # Generate code for each role
        tasks = []
        for role in self.roles:
            tasks.append(role.run())
            
        await asyncio.gather(*tasks)
        
        # Create configuration files
        config_dir = Path(output_dir) / "config"
        for component, options in self.get_configuration_options().items():
            config_file = config_dir / f"{component}.json"
            with open(config_file, "w") as f:
                f.write(str(options))
                
        # Create requirements.txt
        requirements_file = Path(output_dir) / "requirements.txt"
        with open(requirements_file, "w") as f:
            for package, version in self.get_required_dependencies().items():
                f.write(f"{package}{version}\n") 