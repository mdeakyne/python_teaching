"""Generate Jupyter notebooks from skill definitions."""

from pathlib import Path
from typing import Dict, List
import json
from openai import AzureOpenAI

from config import AzureConfig


def generate_notebook(skill: Dict, use_llm: bool = True, model: str = "mini") -> Dict:
    """Generate a Jupyter notebook from skill definition.

    Args:
        skill: Skill dictionary with metadata
        use_llm: Whether to use LLM (True) or template (False)
        model: Which model to use ("chat" or "mini")

    Returns:
        Notebook dictionary (nbformat structure)
    """
    if not use_llm:
        # Simple template for testing
        return {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [f"# {skill['skill_name']}\n"],
                },
                {
                    "cell_type": "code",
                    "metadata": {},
                    "source": ["import pandas as pd\nimport numpy as np"],
                    "outputs": [],
                    "execution_count": None,
                },
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }

    # LLM-based generation
    config = AzureConfig.from_env()
    client = AzureOpenAI(
        api_key=config.api_key,
        api_version=config.api_version,
        azure_endpoint=config.endpoint,
    )

    # Load prompt template
    prompt_path = Path(__file__).parent / "prompts" / "notebook_generation.txt"
    prompt_template = prompt_path.read_text()

    # Format skill details
    skill_details = f"""
Skill Name: {skill["skill_name"]}
Category: {skill["category"]}
Subcategory: {skill.get("subcategory", "N/A")}
Difficulty: {skill["difficulty"]}
Description: {skill["description"]}
Financial Relevance: {skill["financial_relevance"]}/10
Prerequisites: {", ".join(skill.get("prerequisites", []))}
Keywords: {", ".join(skill.get("keywords", []))}
Example Context: {skill.get("example_context", "N/A")}
"""

    practical_title = f"Practical {skill['skill_name']}"

    prompt = prompt_template.format(
        skill_details=skill_details,
        skill_name=skill["skill_name"],
        practical_title=practical_title,
    )

    # Call LLM
    deployment = config.chat_model if model == "chat" else config.mini_model

    print(f"  Generating notebook with {deployment}...")

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": "You are a financial analytics expert creating professional demo notebooks.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=6000,
    )

    content = response.choices[0].message.content.strip()

    # Extract JSON
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()

    try:
        notebook_data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse LLM response: {e}")
        print(f"Response: {content[:500]}")
        # Fallback to template
        return generate_notebook(skill, use_llm=False)

    # Ensure proper nbformat structure
    if "cells" not in notebook_data:
        print("Invalid notebook structure, using fallback")
        return generate_notebook(skill, use_llm=False)

    # Add metadata if missing
    if "metadata" not in notebook_data:
        notebook_data["metadata"] = {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.11.0"},
        }

    if "nbformat" not in notebook_data:
        notebook_data["nbformat"] = 4
        notebook_data["nbformat_minor"] = 5

    # Ensure all code cells have proper structure
    for cell in notebook_data["cells"]:
        if cell["cell_type"] == "code":
            if "outputs" not in cell:
                cell["outputs"] = []
            if "execution_count" not in cell:
                cell["execution_count"] = None
            if "metadata" not in cell:
                cell["metadata"] = {}

    return notebook_data


def save_notebook(notebook: Dict, output_path: str):
    """Save notebook to file.

    Args:
        notebook: Notebook dictionary
        output_path: Path to save .ipynb file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    output_file.write_text(json.dumps(notebook, indent=2))


def generate_multiple_notebooks(
    skills: List[Dict], output_dir: str, model: str = "mini"
) -> List[str]:
    """Generate multiple notebooks from skills.

    Args:
        skills: List of skill dictionaries
        output_dir: Output directory for notebooks
        model: Which model to use

    Returns:
        List of generated notebook paths
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    notebook_paths = []

    for idx, skill in enumerate(skills, 1):
        print(f"\nGenerating notebook {idx}/{len(skills)}: {skill['skill_name']}")

        notebook = generate_notebook(skill, use_llm=True, model=model)

        # Create filename
        filename = f"{idx:02d}_{skill['skill_name'].lower().replace(' ', '_')}.ipynb"
        notebook_path = output_path / filename

        save_notebook(notebook, str(notebook_path))
        print(f"  ✓ Saved to {notebook_path}")

        notebook_paths.append(str(notebook_path))

    return notebook_paths
