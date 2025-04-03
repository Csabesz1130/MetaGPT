#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : startup_engineer.py
"""

from typing import Dict, List, Optional, Set
from pathlib import Path

from metagpt.actions import WriteStartupCode
from metagpt.roles import Role
from metagpt.schema import Message

class StartupEngineer(Role):
    """
    A startup-specifikus kódgenerálásért felelős szerepkör.
    
    Attributes:
        name (str): A mérnök neve
        profile (str): A szerepkör profilja
        goal (str): A szerepkör célja
        constraints (str): A szerepkör korlátai
        tech_stack (Dict[str, str]): A használt technológiák és verzióik
        knowledge_base (Dict[str, str]): A tech stack-specifikus tudásbázis
    """
    
    name: str = "StartupEngineer"
    profile: str = "Startup Engineer"
    goal: str = "Generate modern, scalable, and maintainable startup code"
    constraints: str = (
        "The code should follow modern best practices, be well-documented, "
        "and include proper testing. Focus on rapid development and MVP first, "
        "but ensure the code is scalable for future growth."
    )
    
    def __init__(self, tech_stack: Optional[Dict[str, str]] = None, **kwargs) -> None:
        """
        Inicializálja a StartupEngineer szerepkört.
        
        Args:
            tech_stack (Dict[str, str], optional): A használni kívánt technológiák és verzióik.
                Példa: {"frontend": "react@18.2.0", "backend": "fastapi@0.104.0"}
            **kwargs: További paraméterek az ősosztály számára
        """
        super().__init__(**kwargs)
        self.tech_stack = tech_stack or {}
        self.knowledge_base = {}
        self.set_actions([WriteStartupCode])
        self._watch([WriteStartupCode])
        
    async def analyze_tech_requirements(self, requirements: str) -> Dict[str, str]:
        """
        Elemzi a követelményeket és meghatározza az optimális technológiai választásokat.
        
        Args:
            requirements (str): A projekt követelményei
            
        Returns:
            Dict[str, str]: Az ajánlott technológiák és verzióik
        """
        prompt = f"""
        Analyze the following project requirements and recommend the most suitable technology stack:
        
        Requirements:
        {requirements}
        
        Consider the following aspects:
        1. Scalability needs
        2. Development speed
        3. Team expertise
        4. Community support
        5. Long-term maintenance
        
        Provide recommendations in the following format:
        {{
            "frontend": "framework@version",
            "backend": "framework@version",
            "database": "database@version",
            "deployment": "platform@version"
        }}
        """
        
        response = await self._aask(prompt)
        return eval(response)  # Biztonságos, mivel a válasz formátuma ismert
        
    def load_tech_stack_knowledge(self, tech: str) -> None:
        """
        Betölti a tech stack-specifikus tudásbázist.
        
        Args:
            tech (str): A technológia neve (pl. "react", "fastapi")
        """
        knowledge_path = Path(__file__).parent / "knowledge" / f"{tech}_knowledge.txt"
        if knowledge_path.exists():
            with open(knowledge_path, "r", encoding="utf-8") as f:
                self.knowledge_base[tech] = f.read()
                
    async def _act(self) -> Message | None:
        """
        Végrehajtja a startup kód generálási folyamatot.
        
        Returns:
            Message | None: A generált kód vagy None
        """
        if self.rc.todo is None:
            return None
            
        # Tech stack elemzés és betöltés
        if not self.tech_stack and self.rc.history:
            for msg in self.rc.history:
                if "requirements" in msg.content.lower():
                    self.tech_stack = await self.analyze_tech_requirements(msg.content)
                    break
                    
        # Tudásbázis betöltése
        for tech in self.tech_stack.keys():
            self.load_tech_stack_knowledge(tech)
            
        # Kód generálás a tech stack figyelembevételével
        return await self.rc.todo.run(self.rc.history) 