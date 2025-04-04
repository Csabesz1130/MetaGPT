#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : write_mlops_code.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.actions import Action
from metagpt.schema import Message

class WriteMLOpsCode(Action):
    """
    Action for writing MLOps code.
    
    Attributes:
        name (str): The action name
        context (str): The action context
    """
    
    name: str = "WriteMLOpsCode"
    context: str = "Write code for MLOps"
    
    async def run(self, messages: List[Message]) -> Message:
        """
        Execute the MLOps code writing process.
        
        Args:
            messages (List[Message]): Previous messages
            
        Returns:
            Message: Generated code
        """
        prompt = """
        Write MLOps code with the following features:
        
        1. Model Deployment:
           - Containerization
           - Orchestration
           - Load balancing
           - Auto-scaling
        
        2. Model Versioning:
           - Model registry
           - Version control
           - Rollback capability
           - A/B testing
        
        3. Performance Monitoring:
           - Latency tracking
           - Throughput monitoring
           - Resource utilization
           - Error tracking
        
        4. Automated Deployment:
           - CI/CD pipeline
           - Environment management
           - Configuration management
           - Release management
        
        The code should be:
        - Scalable and reliable
        - Well-documented
        - Easy to maintain
        - Secure and compliant
        """
        
        code = await self._aask(prompt)
        return Message(content=code, role="assistant") 