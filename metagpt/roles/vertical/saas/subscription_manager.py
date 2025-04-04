#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : subscription_manager.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.actions import WriteSubscriptionCode
from metagpt.roles import Role
from metagpt.schema import Message

class SubscriptionManager(Role):
    """
    Role responsible for subscription and billing management in SaaS applications.
    
    Attributes:
        name (str): The manager's name
        profile (str): The role profile
        goal (str): The role's goal
        constraints (str): The role's constraints
        billing_providers (List[str]): Supported billing providers
        subscription_models (List[str]): Supported subscription models
    """
    
    name: str = "SubscriptionManager"
    profile: str = "Subscription Manager"
    goal: str = "Implement robust subscription and billing management"
    constraints: str = (
        "The subscription system should support multiple billing providers, "
        "handle various subscription models, manage trials and upgrades, "
        "and ensure secure payment processing."
    )
    
    billing_providers: List[str] = [
        "stripe",
        "paypal",
        "braintree",
        "paddle"
    ]
    
    subscription_models: List[str] = [
        "freemium",
        "enterprise",
        "usage_based",
        "tiered"
    ]
    
    def __init__(self, 
                 billing_provider: str = "stripe",
                 subscription_model: str = "freemium",
                 **kwargs) -> None:
        """
        Initialize the SubscriptionManager role.
        
        Args:
            billing_provider (str): The billing provider to use
            subscription_model (str): The subscription model to implement
            **kwargs: Additional parameters for the parent class
        """
        super().__init__(**kwargs)
        self.billing_provider = billing_provider
        self.subscription_model = subscription_model
        self.set_actions([WriteSubscriptionCode])
        self._watch([WriteSubscriptionCode])
        
    async def analyze_subscription_requirements(self, requirements: str) -> Dict[str, str]:
        """
        Analyze requirements and determine optimal subscription setup.
        
        Args:
            requirements (str): Project requirements
            
        Returns:
            Dict[str, str]: Recommended subscription configuration
        """
        prompt = f"""
        Analyze the following SaaS requirements and recommend the most suitable subscription setup:
        
        Requirements:
        {requirements}
        
        Consider the following aspects:
        1. Target market and pricing strategy
        2. Feature access requirements
        3. Payment processing needs
        4. Trial period requirements
        5. Upgrade/downgrade flexibility
        
        Provide recommendations in the following format:
        {{
            "billing_provider": "provider_name",
            "subscription_model": "model_name",
            "trial_period": "days",
            "pricing_tiers": ["tier1", "tier2", "tier3"],
            "payment_methods": ["method1", "method2"]
        }}
        """
        
        response = await self._aask(prompt)
        return eval(response)
        
    async def _act(self) -> Message | None:
        """
        Execute the subscription management implementation process.
        
        Returns:
            Message | None: Generated code or None
        """
        if self.rc.todo is None:
            return None
            
        # Analyze requirements if not already configured
        if not self.billing_provider and self.rc.history:
            for msg in self.rc.history:
                if "requirements" in msg.content.lower():
                    config = await self.analyze_subscription_requirements(msg.content)
                    self.billing_provider = config["billing_provider"]
                    self.subscription_model = config["subscription_model"]
                    break
                    
        # Generate subscription management code
        return await self.rc.todo.run(self.rc.history) 