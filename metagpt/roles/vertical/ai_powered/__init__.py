#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : __init__.py
"""

from metagpt.roles.vertical.ai_powered.data_pipeline_engineer import DataPipelineEngineer
from metagpt.roles.vertical.ai_powered.mlops_specialist import MLOpsSpecialist
from metagpt.roles.vertical.ai_powered.ai_feature_designer import AIFeatureDesigner
from metagpt.roles.vertical.ai_powered.data_privacy_officer import DataPrivacyOfficer

__all__ = [
    "DataPipelineEngineer",
    "MLOpsSpecialist",
    "AIFeatureDesigner",
    "DataPrivacyOfficer"
] 