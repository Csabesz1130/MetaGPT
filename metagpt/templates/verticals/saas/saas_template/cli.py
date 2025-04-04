#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/3
@Author  : csaba
@File    : cli.py
"""

import argparse
import asyncio
from typing import Optional

from saas_template import SAAS_Template

def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Generate a SaaS application template"
    )
    
    parser.add_argument(
        "--billing-model",
        type=str,
        default="subscription",
        choices=["subscription", "usage-based", "freemium"],
        help="Billing model to use"
    )
    
    parser.add_argument(
        "--onboarding-type",
        type=str,
        default="guided_tour",
        choices=["guided_tour", "interactive_tutorial", "video_walkthrough"],
        help="Onboarding type to implement"
    )
    
    parser.add_argument(
        "--metrics-type",
        type=str,
        default="user_engagement",
        choices=["user_engagement", "feature_usage", "performance"],
        help="Metrics type to track"
    )
    
    parser.add_argument(
        "--retention-strategy",
        type=str,
        default="proactive_engagement",
        choices=["proactive_engagement", "feedback_collection", "support_automation"],
        help="Retention strategy to employ"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Output directory for generated code"
    )
    
    return parser.parse_args()

async def main() -> None:
    """
    Main entry point for the CLI.
    """
    args = parse_args()
    
    template = SAAS_Template(
        billing_model=args.billing_model,
        onboarding_type=args.onboarding_type,
        metrics_type=args.metrics_type,
        retention_strategy=args.retention_strategy
    )
    
    await template.generate(args.output_dir)

if __name__ == "__main__":
    asyncio.run(main()) 