"""Skill extraction from markdown content using LLM."""

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional

from config import AzureConfig
from openai import AzureOpenAI


@dataclass
class Skill:
    """Represents an extracted technical skill."""

    skill_id: str
    skill_name: str
    category: str
    subcategory: str
    description: str
    source_chapter: str
    difficulty: str
    prerequisites: List[str]
    financial_relevance: int
    keywords: List[str]
    example_context: str

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


def extract_skills_from_markdown(
    markdown_content: str, book_title: str, use_llm: bool = True, model: str = "chat"
) -> List[Skill]:
    """Extract skills from markdown content.

    Args:
        markdown_content: Markdown text to analyze
        book_title: Title of the source book
        use_llm: Whether to use LLM (True) or rule-based extraction (False)
        model: Which model to use ("chat" or "mini")

    Returns:
        List of extracted Skill objects
    """
    if not use_llm:
        # Simple rule-based extraction for testing
        skills = []
        # Match ## headers, allowing for leading whitespace
        chapters = re.findall(r"^\s*##\s+(.+)$", markdown_content, re.MULTILINE)

        for idx, chapter in enumerate(chapters, 1):
            skill = Skill(
                skill_id=f"rule_{idx:03d}",
                skill_name=chapter,
                category="unknown",
                subcategory="unknown",
                description=f"Skill from: {chapter}",
                source_chapter=chapter,
                difficulty="intermediate",
                prerequisites=[],
                financial_relevance=5,
                keywords=[],
                example_context="",
            )
            skills.append(skill)

        return skills

    # LLM-based extraction
    config = AzureConfig.from_env()
    client = AzureOpenAI(
        api_key=config.api_key,
        api_version=config.api_version,
        azure_endpoint=config.endpoint,
    )

    # Load prompt template
    prompt_path = Path(__file__).parent / "prompts" / "skill_extraction.txt"
    prompt_template = prompt_path.read_text()

    # Format prompt
    prompt = prompt_template.format(
        book_title=book_title,
        content=markdown_content[:8000],  # Limit content size
    )

    # Call LLM
    deployment = config.chat_model if model == "chat" else config.mini_model

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": "You are a technical skill extraction expert.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=4000,
    )

    # Parse response
    content = response.choices[0].message.content.strip()

    # Extract JSON from response (remove markdown code blocks if present)
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()

    try:
        skills_data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse LLM response: {e}")
        print(f"Response: {content[:500]}")
        return []

    # Convert to Skill objects
    skills = []
    for idx, skill_data in enumerate(skills_data, 1):
        skill = Skill(
            skill_id=f"{book_title.lower().replace(' ', '_')[:20]}_{idx:03d}",
            skill_name=skill_data.get("skill_name", ""),
            category=skill_data.get("category", "unknown"),
            subcategory=skill_data.get("subcategory", ""),
            description=skill_data.get("description", ""),
            source_chapter=skill_data.get("source_chapter", ""),
            difficulty=skill_data.get("difficulty", "intermediate"),
            prerequisites=skill_data.get("prerequisites", []),
            financial_relevance=skill_data.get("financial_relevance", 5),
            keywords=skill_data.get("keywords", []),
            example_context=skill_data.get("example_context", ""),
        )
        skills.append(skill)

    return skills


def save_skills_to_json(
    skills: List[Skill], output_path: str, book_title: str, extraction_date: str
):
    """Save skills to JSON file.

    Args:
        skills: List of Skill objects
        output_path: Path to output JSON file
        book_title: Title of source book
        extraction_date: Date of extraction (YYYY-MM-DD)
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "book_title": book_title,
        "extraction_date": extraction_date,
        "skills": [skill.to_dict() for skill in skills],
    }

    output_file.write_text(json.dumps(data, indent=2))
