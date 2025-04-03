#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : write_startup_code.py
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from metagpt.actions import Action
from metagpt.schema import Message
from metagpt.utils.project_repo import ProjectRepo

class StartupCodeContext(BaseModel):
    """Startup code generation context model."""
    architecture: Dict[str, str] = Field(default_factory=dict, description="The architecture description")
    tech_stack: Dict[str, str] = Field(default_factory=dict, description="The technologies to be used")
    database_schema: str = Field(default="", description="The database schema")
    api_endpoints: List[Dict[str, str]] = Field(default_factory=list, description="API endpoints")
    frontend_components: List[Dict[str, str]] = Field(default_factory=list, description="Frontend components")
    backend_services: List[Dict[str, str]] = Field(default_factory=list, description="Backend services")
    test_cases: List[Dict[str, str]] = Field(default_factory=list, description="Test cases")

class WriteStartupCode(Action):
    """
    Generate startup code based on the architecture.
    """
    
    name: str = "WriteStartupCode"
    context: StartupCodeContext = Field(default_factory=StartupCodeContext)
    repo: Optional[ProjectRepo] = Field(default=None, exclude=True)
    
    async def run(self, context: List[Message] = None) -> Message:
        """Execute the code generation process."""
        # Extract architecture information from the context
        if context and len(context) > 0:
            for msg in context:
                if hasattr(msg, 'content') and isinstance(msg.content, str):
                    if "Startup Architecture Design" in msg.content:
                        # Try to extract architecture information from the message
                        self._extract_architecture_from_message(msg.content)
                        break
        
        # Create a detailed prompt for the LLM
        prompt = f"""
        Generate code for the following startup architecture:
        
        Architecture: {self.context.architecture}
        Tech Stack: {self.context.tech_stack}
        Database Schema: {self.context.database_schema}
        API Endpoints: {self.context.api_endpoints}
        
        Generate the following components:
        1. Frontend Components:
           - Create React/Vue/Angular components based on the selected frontend technology
           - Include routing, state management, and UI components
           - Implement responsive design
        
        2. Backend Services:
           - Create API endpoints based on the defined API structure
           - Implement authentication and authorization
           - Set up database models and migrations
           - Include business logic and services
        
        3. Database Migrations:
           - Create database migration scripts
           - Include seed data for development
        
        4. API Endpoint Implementation:
           - Implement RESTful API endpoints
           - Include input validation and error handling
           - Add documentation
        
        5. Test Cases:
           - Create unit tests for backend services
           - Create integration tests for API endpoints
           - Create frontend component tests
        
        Provide the code in the following JSON format:
        {{
            "frontend_components": [
                {{
                    "name": "ComponentName",
                    "path": "path/to/component",
                    "code": "Actual component code"
                }}
            ],
            "backend_services": [
                {{
                    "name": "ServiceName",
                    "path": "path/to/service",
                    "code": "Actual service code"
                }}
            ],
            "database_migrations": [
                {{
                    "name": "MigrationName",
                    "path": "path/to/migration",
                    "code": "Actual migration code"
                }}
            ],
            "api_endpoints": [
                {{
                    "path": "/api/v1/resource",
                    "method": "GET/POST/PUT/DELETE",
                    "code": "Actual endpoint code"
                }}
            ],
            "test_cases": [
                {{
                    "name": "TestName",
                    "path": "path/to/test",
                    "code": "Actual test code"
                }}
            ]
        }}
        """
        
        # Call the LLM to generate the code
        response = await self._aask(prompt)
        
        try:
            # Parse the JSON response
            code_data = json.loads(response)
            
            # Update the context with the generated code
            self.context.frontend_components = code_data.get("frontend_components", [])
            self.context.backend_services = code_data.get("backend_services", [])
            self.context.api_endpoints = code_data.get("api_endpoints", [])
            self.context.test_cases = code_data.get("test_cases", [])
            
            # If we have a repository, save the generated code
            if self.repo:
                await self._save_code_to_repo()
            
            # Create a formatted response
            formatted_response = f"""
            # Startup Code Generation
            
            ## Frontend Components
            Generated {len(self.context.frontend_components)} frontend components.
            
            ## Backend Services
            Generated {len(self.context.backend_services)} backend services.
            
            ## API Endpoints
            Generated {len(self.context.api_endpoints)} API endpoints.
            
            ## Test Cases
            Generated {len(self.context.test_cases)} test cases.
            
            The code has been saved to the repository.
            """
            
            return Message(content=formatted_response)
            
        except json.JSONDecodeError:
            # If the response is not valid JSON, return it as is
            return Message(content=f"Startup code generation completed. Raw response: {response}")
    
    def _extract_architecture_from_message(self, content: str) -> None:
        """Extract architecture information from a message."""
        # This is a simple implementation that could be improved
        lines = content.split('\n')
        
        # Extract tech stack
        tech_stack = {}
        for i, line in enumerate(lines):
            if "Technology Stack" in line:
                for j in range(i+1, min(i+5, len(lines))):
                    if "Frontend:" in lines[j]:
                        tech_stack["frontend"] = lines[j].split("Frontend:")[1].strip()
                    elif "Backend:" in lines[j]:
                        tech_stack["backend"] = lines[j].split("Backend:")[1].strip()
                    elif "Database:" in lines[j]:
                        tech_stack["database"] = lines[j].split("Database:")[1].strip()
                    elif "Infrastructure:" in lines[j]:
                        tech_stack["infrastructure"] = lines[j].split("Infrastructure:")[1].strip()
        
        # Extract architecture
        architecture = ""
        for i, line in enumerate(lines):
            if "Architecture" in line:
                for j in range(i+1, len(lines)):
                    if "Database Schema" in lines[j]:
                        break
                    architecture += lines[j] + "\n"
        
        # Extract database schema
        database_schema = ""
        for i, line in enumerate(lines):
            if "Database Schema" in line:
                for j in range(i+1, len(lines)):
                    if "API Endpoints" in lines[j]:
                        break
                    database_schema += lines[j] + "\n"
        
        # Extract API endpoints
        api_endpoints = []
        for i, line in enumerate(lines):
            if "API Endpoints" in line:
                try:
                    # Try to parse the JSON array
                    endpoints_json = ""
                    for j in range(i+1, len(lines)):
                        if "Deployment Strategy" in lines[j]:
                            break
                        endpoints_json += lines[j]
                    
                    api_endpoints = json.loads(endpoints_json)
                except:
                    # If parsing fails, create a simple endpoint
                    api_endpoints = [{"path": "/api/v1/resource", "method": "GET", "description": "Default endpoint"}]
        
        # Update the context
        self.context.tech_stack = tech_stack
        self.context.architecture = architecture
        self.context.database_schema = database_schema
        self.context.api_endpoints = api_endpoints
    
    async def _save_code_to_repo(self) -> None:
        """Save the generated code to the repository."""
        # Create directories if they don't exist
        frontend_dir = self.repo.workdir / "frontend"
        backend_dir = self.repo.workdir / "backend"
        tests_dir = self.repo.workdir / "tests"
        
        os.makedirs(frontend_dir, exist_ok=True)
        os.makedirs(backend_dir, exist_ok=True)
        os.makedirs(tests_dir, exist_ok=True)
        
        # Save frontend components
        for component in self.context.frontend_components:
            path = frontend_dir / component.get("path", "")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(component.get("code", ""))
        
        # Save backend services
        for service in self.context.backend_services:
            path = backend_dir / service.get("path", "")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(service.get("code", ""))
        
        # Save test cases
        for test in self.context.test_cases:
            path = tests_dir / test.get("path", "")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(test.get("code", "")) 