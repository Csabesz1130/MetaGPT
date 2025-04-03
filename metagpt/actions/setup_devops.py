#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : setup_devops.py
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from metagpt.actions import Action
from metagpt.schema import Message
from metagpt.utils.project_repo import ProjectRepo

class DevOpsContext(BaseModel):
    """DevOps setup context model."""
    tech_stack: Dict[str, str] = Field(default_factory=dict, description="The technologies to be used")
    ci_cd_pipeline: Dict[str, str] = Field(default_factory=dict, description="CI/CD pipeline configuration")
    containerization: Dict[str, str] = Field(default_factory=dict, description="Containerization configuration")
    infrastructure: Dict[str, str] = Field(default_factory=dict, description="Infrastructure configuration")
    monitoring: Dict[str, str] = Field(default_factory=dict, description="Monitoring configuration")
    security: Dict[str, str] = Field(default_factory=dict, description="Security configuration")

class SetupDevOps(Action):
    """
    Set up DevOps environment for the startup.
    """
    
    name: str = "SetupDevOps"
    context: DevOpsContext = Field(default_factory=DevOpsContext)
    repo: Optional[ProjectRepo] = Field(default=None, exclude=True)
    
    async def run(self, context: List[Message] = None) -> Message:
        """Execute the DevOps setup process."""
        # Extract technology stack information from the context
        if context and len(context) > 0:
            for msg in context:
                if hasattr(msg, 'content') and isinstance(msg.content, str):
                    if "Technology Stack" in msg.content:
                        # Try to extract technology stack information from the message
                        self._extract_tech_stack_from_message(msg.content)
                        break
        
        # Create a detailed prompt for the LLM
        prompt = f"""
        Set up a DevOps environment for a startup with the following technology stack:
        
        Tech Stack: {self.context.tech_stack}
        
        Consider the following aspects:
        1. CI/CD Pipeline:
           - Choose appropriate CI/CD tools (GitHub Actions, GitLab CI, Jenkins, etc.)
           - Define build, test, and deployment stages
           - Set up automated testing and quality checks
        
        2. Containerization:
           - Create Dockerfile for the application
           - Set up Docker Compose for local development
           - Consider Kubernetes for production
        
        3. Infrastructure as Code:
           - Use Terraform or CloudFormation for infrastructure
           - Define cloud resources (VMs, databases, etc.)
           - Set up networking and security
        
        4. Monitoring and Logging:
           - Set up monitoring tools (Prometheus, Grafana, etc.)
           - Configure logging (ELK Stack, etc.)
           - Define alerts and dashboards
        
        5. Security:
           - Implement security best practices
           - Set up secrets management
           - Configure access control
        
        Provide the DevOps setup in the following JSON format:
        {{
            "ci_cd_pipeline": {{
                "tool": "Selected CI/CD tool",
                "config": "CI/CD configuration"
            }},
            "containerization": {{
                "dockerfile": "Dockerfile content",
                "docker_compose": "Docker Compose content",
                "kubernetes": "Kubernetes manifests"
            }},
            "infrastructure": {{
                "tool": "Selected IaC tool",
                "config": "Infrastructure configuration"
            }},
            "monitoring": {{
                "tool": "Selected monitoring tool",
                "config": "Monitoring configuration"
            }},
            "security": {{
                "secrets_management": "Secrets management configuration",
                "access_control": "Access control configuration"
            }}
        }}
        """
        
        # Call the LLM to generate the DevOps setup
        response = await self._aask(prompt)
        
        try:
            # Parse the JSON response
            devops_data = json.loads(response)
            
            # Update the context with the generated DevOps setup
            self.context.ci_cd_pipeline = devops_data.get("ci_cd_pipeline", {})
            self.context.containerization = devops_data.get("containerization", {})
            self.context.infrastructure = devops_data.get("infrastructure", {})
            self.context.monitoring = devops_data.get("monitoring", {})
            self.context.security = devops_data.get("security", {})
            
            # If we have a repository, save the DevOps setup
            if self.repo:
                await self._save_devops_to_repo()
            
            # Create a formatted response
            formatted_response = f"""
            # DevOps Setup
            
            ## CI/CD Pipeline
            Tool: {self.context.ci_cd_pipeline.get("tool", "Not specified")}
            
            ## Containerization
            Dockerfile and Docker Compose have been created.
            
            ## Infrastructure
            Tool: {self.context.infrastructure.get("tool", "Not specified")}
            
            ## Monitoring
            Tool: {self.context.monitoring.get("tool", "Not specified")}
            
            ## Security
            Secrets management and access control have been configured.
            
            The DevOps setup has been saved to the repository.
            """
            
            return Message(content=formatted_response)
            
        except json.JSONDecodeError:
            # If the response is not valid JSON, return it as is
            return Message(content=f"DevOps setup completed. Raw response: {response}")
    
    def _extract_tech_stack_from_message(self, content: str) -> None:
        """Extract technology stack information from a message."""
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
        
        # Update the context
        self.context.tech_stack = tech_stack
    
    async def _save_devops_to_repo(self) -> None:
        """Save the DevOps setup to the repository."""
        # Create directories if they don't exist
        devops_dir = self.repo.workdir / "devops"
        os.makedirs(devops_dir, exist_ok=True)
        
        # Save CI/CD configuration
        if self.context.ci_cd_pipeline:
            ci_cd_dir = devops_dir / "ci-cd"
            os.makedirs(ci_cd_dir, exist_ok=True)
            
            # Save GitHub Actions workflow
            if self.context.ci_cd_pipeline.get("tool", "").lower() == "github actions":
                workflow_file = ci_cd_dir / ".github/workflows/main.yml"
                os.makedirs(os.path.dirname(workflow_file), exist_ok=True)
                with open(workflow_file, "w") as f:
                    f.write(self.context.ci_cd_pipeline.get("config", ""))
            
            # Save GitLab CI configuration
            elif self.context.ci_cd_pipeline.get("tool", "").lower() == "gitlab ci":
                gitlab_ci_file = ci_cd_dir / ".gitlab-ci.yml"
                with open(gitlab_ci_file, "w") as f:
                    f.write(self.context.ci_cd_pipeline.get("config", ""))
            
            # Save Jenkins pipeline
            elif self.context.ci_cd_pipeline.get("tool", "").lower() == "jenkins":
                jenkins_file = ci_cd_dir / "Jenkinsfile"
                with open(jenkins_file, "w") as f:
                    f.write(self.context.ci_cd_pipeline.get("config", ""))
        
        # Save containerization configuration
        if self.context.containerization:
            container_dir = devops_dir / "container"
            os.makedirs(container_dir, exist_ok=True)
            
            # Save Dockerfile
            if "dockerfile" in self.context.containerization:
                dockerfile = container_dir / "Dockerfile"
                with open(dockerfile, "w") as f:
                    f.write(self.context.containerization.get("dockerfile", ""))
            
            # Save Docker Compose
            if "docker_compose" in self.context.containerization:
                docker_compose = container_dir / "docker-compose.yml"
                with open(docker_compose, "w") as f:
                    f.write(self.context.containerization.get("docker_compose", ""))
            
            # Save Kubernetes manifests
            if "kubernetes" in self.context.containerization:
                k8s_dir = container_dir / "kubernetes"
                os.makedirs(k8s_dir, exist_ok=True)
                with open(k8s_dir / "deployment.yml", "w") as f:
                    f.write(self.context.containerization.get("kubernetes", ""))
        
        # Save infrastructure configuration
        if self.context.infrastructure:
            infra_dir = devops_dir / "infrastructure"
            os.makedirs(infra_dir, exist_ok=True)
            
            # Save Terraform configuration
            if self.context.infrastructure.get("tool", "").lower() == "terraform":
                terraform_file = infra_dir / "main.tf"
                with open(terraform_file, "w") as f:
                    f.write(self.context.infrastructure.get("config", ""))
            
            # Save CloudFormation template
            elif self.context.infrastructure.get("tool", "").lower() == "cloudformation":
                cloudformation_file = infra_dir / "template.yml"
                with open(cloudformation_file, "w") as f:
                    f.write(self.context.infrastructure.get("config", ""))
        
        # Save monitoring configuration
        if self.context.monitoring:
            monitoring_dir = devops_dir / "monitoring"
            os.makedirs(monitoring_dir, exist_ok=True)
            
            # Save Prometheus configuration
            if self.context.monitoring.get("tool", "").lower() == "prometheus":
                prometheus_file = monitoring_dir / "prometheus.yml"
                with open(prometheus_file, "w") as f:
                    f.write(self.context.monitoring.get("config", ""))
        
        # Save security configuration
        if self.context.security:
            security_dir = devops_dir / "security"
            os.makedirs(security_dir, exist_ok=True)
            
            # Save secrets management configuration
            if "secrets_management" in self.context.security:
                secrets_file = security_dir / "secrets.yml"
                with open(secrets_file, "w") as f:
                    f.write(self.context.security.get("secrets_management", ""))
            
            # Save access control configuration
            if "access_control" in self.context.security:
                access_file = security_dir / "access.yml"
                with open(access_file, "w") as f:
                    f.write(self.context.security.get("access_control", "")) 