#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : write_startup_architecture.py
"""

import json
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from metagpt.actions import Action
from metagpt.schema import Message

class StartupArchitectureContext(BaseModel):
    """Startup architecture context model."""
    idea: str = Field(default="", description="The startup idea")
    tech_stack: Dict[str, str] = Field(default_factory=dict, description="The technologies to be used")
    architecture: str = Field(default="", description="The architecture description")
    database_schema: str = Field(default="", description="The database schema")
    api_endpoints: List[Dict[str, str]] = Field(default_factory=list, description="API endpoints")
    deployment_strategy: str = Field(default="", description="Deployment strategy")
    scaling_strategy: str = Field(default="", description="Scaling strategy")

class WriteStartupArchitecture(Action):
    """
    Design and document startup architecture.
    """
    
    name: str = "WriteStartupArchitecture"
    context: StartupArchitectureContext = Field(default_factory=StartupArchitectureContext)
    
    async def run(self, context: List[Message] = None) -> Message:
        """Execute the architecture design process."""
        # Extract the startup idea from the context
        if context and len(context) > 0:
            for msg in context:
                if hasattr(msg, 'content') and isinstance(msg.content, str):
                    if "startup idea" in msg.content.lower() or "project idea" in msg.content.lower():
                        self.context.idea = msg.content
                        break
        
        # Create a detailed prompt for the LLM
        prompt = f"""
        Design a modern startup architecture for the following idea: {self.context.idea}
        
        Consider the following aspects:
        1. Technology Stack Selection:
           - Frontend: Choose a modern framework (React, Vue, Angular, etc.)
           - Backend: Select appropriate frameworks (Node.js, Django, FastAPI, etc.)
           - Database: Choose database types (SQL, NoSQL, etc.)
           - Infrastructure: Cloud providers, containers, etc.
        
        2. Architecture Type:
           - Decide between monolithic or microservices
           - Consider the trade-offs for a startup
           - Focus on MVP first, but ensure scalability
        
        3. Database Schema Design:
           - Design the core data models
           - Consider relationships and constraints
           - Plan for future expansion
        
        4. API Endpoints Definition:
           - Define RESTful API endpoints
           - Include authentication/authorization
           - Consider versioning strategy
        
        5. Deployment Strategy:
           - CI/CD pipeline
           - Containerization approach
           - Environment management
        
        6. Scaling Strategy:
           - Horizontal vs vertical scaling
           - Load balancing approach
           - Caching strategy
        
        Provide a comprehensive architecture design in the following JSON format:
        {{
            "idea": "The startup idea",
            "tech_stack": {{
                "frontend": "Selected frontend technology",
                "backend": "Selected backend technology",
                "database": "Selected database technology",
                "infrastructure": "Selected infrastructure technology"
            }},
            "architecture": "Detailed architecture description",
            "database_schema": "Database schema design",
            "api_endpoints": [
                {{
                    "path": "/api/v1/resource",
                    "method": "GET/POST/PUT/DELETE",
                    "description": "Endpoint description"
                }}
            ],
            "deployment_strategy": "Deployment strategy details",
            "scaling_strategy": "Scaling strategy details"
        }}
        """
        
        # Call the LLM to generate the architecture design
        response = await self._aask(prompt)
        
        try:
            # Parse the JSON response
            architecture_data = json.loads(response)
            
            # Update the context with the generated architecture
            self.context.idea = architecture_data.get("idea", self.context.idea)
            self.context.tech_stack = architecture_data.get("tech_stack", {})
            self.context.architecture = architecture_data.get("architecture", "")
            self.context.database_schema = architecture_data.get("database_schema", "")
            self.context.api_endpoints = architecture_data.get("api_endpoints", [])
            self.context.deployment_strategy = architecture_data.get("deployment_strategy", "")
            self.context.scaling_strategy = architecture_data.get("scaling_strategy", "")
            
            # Create a formatted response
            formatted_response = f"""
            # Startup Architecture Design
            
            ## Idea
            {self.context.idea}
            
            ## Technology Stack
            - Frontend: {self.context.tech_stack.get('frontend', 'Not specified')}
            - Backend: {self.context.tech_stack.get('backend', 'Not specified')}
            - Database: {self.context.tech_stack.get('database', 'Not specified')}
            - Infrastructure: {self.context.tech_stack.get('infrastructure', 'Not specified')}
            
            ## Architecture
            {self.context.architecture}
            
            ## Database Schema
            {self.context.database_schema}
            
            ## API Endpoints
            {json.dumps(self.context.api_endpoints, indent=2)}
            
            ## Deployment Strategy
            {self.context.deployment_strategy}
            
            ## Scaling Strategy
            {self.context.scaling_strategy}
            """
            
            return Message(content=formatted_response)
            
        except json.JSONDecodeError:
            # If the response is not valid JSON, return it as is
            return Message(content=f"Startup architecture design completed. Raw response: {response}") 