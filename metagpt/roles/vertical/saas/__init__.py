#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : __init__.py
"""

from metagpt.roles.vertical.saas.subscription_manager import SubscriptionManager
from metagpt.roles.vertical.saas.onboarding_specialist import OnboardingSpecialist
from metagpt.roles.vertical.saas.analytics_engineer import AnalyticsEngineer
from metagpt.roles.vertical.saas.customer_success_agent import CustomerSuccessAgent

__all__ = [
    "SubscriptionManager",
    "OnboardingSpecialist",
    "AnalyticsEngineer",
    "CustomerSuccessAgent"
] 