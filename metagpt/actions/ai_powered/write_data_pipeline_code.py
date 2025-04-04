#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : write_data_pipeline_code.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.actions import Action
from metagpt.schema import Message

class WriteDataPipelineCode(Action):
    """
    Action for writing data pipeline code.
    
    Attributes:
        name (str): The action name
        context (str): The action context
    """
    
    name: str = "WriteDataPipelineCode"
    context: str = "Write code for data pipeline"
    
    async def run(self, messages: List[Message]) -> Message:
        """
        Execute the data pipeline code writing process.
        
        Args:
            messages (List[Message]): Previous messages
            
        Returns:
            Message: Generated code
        """
        prompt = """
        Write data pipeline code with the following features:
        
        1. Data Ingestion:
           - Support for multiple data sources
           - Data validation and cleaning
           - Error handling and retry logic
           - Progress tracking and logging
        
        2. Data Transformation:
           - Feature engineering
           - Data normalization
           - Data enrichment
           - Data quality checks
        
        3. Data Validation:
           - Schema validation
           - Data type checking
           - Range validation
           - Consistency checks
        
        4. Data Monitoring:
           - Performance metrics
           - Error tracking
           - Data quality metrics
           - Resource utilization
        
        The code should be:
        - Scalable and efficient
        - Well-documented
        - Easy to maintain
        - Robust to failures
        """
        
        code = await self._aask(prompt)
        return Message(content=code, role="assistant") 