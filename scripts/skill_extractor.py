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
    tracks: Optional[List[str]] = None
    key_concepts: Optional[List[str]] = None
    learning_resources: Optional[List[str]] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    def to_markdown(self, book_name: str = "") -> str:
        """Convert skill to Claude-style markdown format.

        Args:
            book_name: Name of the source book for learning resources

        Returns:
            Markdown-formatted skill content
        """
        # Generate slug from skill name
        slug = self.skill_name.lower().replace(" ", "-").replace("/", "-")

        # Build markdown content
        lines = [
            f"# {self.skill_name}",
            "",
            f"**Tracks**: {', '.join(self.tracks or ['financial-analytics'])}",
            f"**Difficulty**: {self.difficulty}",
            f"**Category**: {self.category}",
            "",
            "## Description",
            "",
            self.description,
            "",
        ]

        # Add key concepts
        if self.key_concepts:
            lines.extend(
                [
                    "## Key Concepts",
                    "",
                ]
            )
            for concept in self.key_concepts:
                lines.append(f"- {concept}")
            lines.append("")

        # Add prerequisites
        if self.prerequisites:
            lines.extend(
                [
                    "## Prerequisites",
                    "",
                ]
            )
            for prereq in self.prerequisites:
                # Convert to markdown link format
                prereq_slug = prereq.lower().replace(" ", "-").replace("/", "-")
                lines.append(f"- [{prereq}](./{prereq_slug}.md)")
            lines.append("")

        # Add learning resources
        if self.learning_resources or self.source_chapter:
            lines.extend(
                [
                    "## Learning Resources",
                    "",
                ]
            )
            if self.learning_resources:
                for resource in self.learning_resources:
                    lines.append(f"- {resource}")
            elif self.source_chapter and book_name:
                lines.append(f"- **{book_name}**: {self.source_chapter}")
            lines.append("")

        # Add footer
        lines.extend(
            [
                "---",
                "",
                f"*Source: {book_name or 'unknown'}*",
                "",
            ]
        )

        return "\n".join(lines)


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
            tracks=skill_data.get("tracks", ["financial-analytics"]),
            key_concepts=skill_data.get("key_concepts", []),
            learning_resources=skill_data.get("learning_resources", []),
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


def save_skills_to_markdown(skills: List[Skill], output_dir: str, book_title: str):
    """Save skills as individual markdown files.

    Args:
        skills: List of Skill objects
        output_dir: Directory to save markdown files
        book_title: Title of source book for references
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Convert book title to a clean book name for references
    book_name = book_title.lower().replace(" ", "-").replace("_", "-")

    for skill in skills:
        # Generate filename from skill name
        filename = skill.skill_name.lower().replace(" ", "-").replace("/", "-")
        filename = filename.replace("(", "").replace(")", "").replace(":", "")
        filename = f"{filename}.md"

        # Generate markdown content
        markdown_content = skill.to_markdown(book_name=book_name)

        # Write to file
        file_path = output_path / filename
        file_path.write_text(markdown_content)
