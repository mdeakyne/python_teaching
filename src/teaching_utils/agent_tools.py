"""
Agent Tool Functions for PDF-to-Skills Pipeline

Provides @ai_function decorated tools that agents can use for PDF processing,
skill extraction, validation, and organization tasks.
"""

import json
import re
from pathlib import Path
from typing import Annotated, List, Dict, Any, Optional

from pydantic import BaseModel, Field
from pypdf import PdfReader
from rich.console import Console


console = Console()


# Note: @ai_function decorator from agent_framework
# Will be imported when agent_framework package is installed
# For now, we'll define tools as regular functions with proper type hints
# and add decorators in the migration phase


def extract_pdf_text(pdf_path: Annotated[str, Field(description="Path to PDF file")]) -> str:
    """
    Extract all text content from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text as a single string
    """
    try:
        path = Path(pdf_path)
        if not path.exists():
            return f"Error: PDF file not found at {pdf_path}"

        reader = PdfReader(path)
        text_chunks = []

        for page in reader.pages:
            text = page.extract_text()
            if text.strip():
                text_chunks.append(text)

        result = "\n\n".join(text_chunks)
        console.print(f"[dim]Extracted {len(text_chunks)} pages from {path.name}[/dim]")
        return result

    except Exception as e:
        return f"Error extracting PDF text: {str(e)}"


def chunk_content(
    content: Annotated[str, Field(description="Text content to chunk")],
    chunk_size: Annotated[int, Field(description="Maximum chunk size in characters")] = 8000,
    overlap: Annotated[int, Field(description="Overlap between chunks")] = 200
) -> List[str]:
    """
    Split content into overlapping chunks for processing.

    Args:
        content: Text to split
        chunk_size: Maximum characters per chunk
        overlap: Overlap size between consecutive chunks

    Returns:
        List of text chunks
    """
    if not content:
        return []

    chunks = []
    start = 0
    content_length = len(content)

    while start < content_length:
        end = start + chunk_size

        # Try to break at paragraph boundaries
        if end < content_length:
            # Look for paragraph break near the end
            search_start = max(start, end - 200)
            paragraph_break = content.rfind('\n\n', search_start, end)

            if paragraph_break > start:
                end = paragraph_break

        chunk = content[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move to next chunk with overlap
        start = end - overlap if end < content_length else content_length

    console.print(f"[dim]Split content into {len(chunks)} chunks[/dim]")
    return chunks


def validate_skill_structure(
    skill_data: Annotated[str, Field(description="JSON string of skill data")]
) -> Dict[str, Any]:
    """
    Validate that a skill has all required fields and proper structure.

    Args:
        skill_data: JSON string containing skill information

    Returns:
        Validation result with is_valid flag and error messages
    """
    required_fields = [
        "name", "description", "category", "difficulty",
        "key_concepts", "source_section"
    ]

    valid_difficulties = ["beginner", "intermediate", "advanced"]

    try:
        skill = json.loads(skill_data)

        errors = []

        # Check required fields
        for field in required_fields:
            if field not in skill:
                errors.append(f"Missing required field: {field}")

        # Validate difficulty level
        if "difficulty" in skill and skill["difficulty"] not in valid_difficulties:
            errors.append(
                f"Invalid difficulty: {skill['difficulty']}. "
                f"Must be one of: {', '.join(valid_difficulties)}"
            )

        # Validate key_concepts is a non-empty list
        if "key_concepts" in skill:
            if not isinstance(skill["key_concepts"], list):
                errors.append("key_concepts must be a list")
            elif len(skill["key_concepts"]) == 0:
                errors.append("key_concepts cannot be empty")

        # Validate name and description have content
        if "name" in skill and not skill["name"].strip():
            errors.append("name cannot be empty")

        if "description" in skill and not skill["description"].strip():
            errors.append("description cannot be empty")

        result = {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "skill": skill if len(errors) == 0 else None
        }

        return result

    except json.JSONDecodeError as e:
        return {
            "is_valid": False,
            "errors": [f"Invalid JSON: {str(e)}"],
            "skill": None
        }


def check_skill_similarity(
    skill1_name: Annotated[str, Field(description="Name of first skill")],
    skill2_name: Annotated[str, Field(description="Name of second skill")],
    threshold: Annotated[float, Field(description="Similarity threshold (0-1)")] = 0.8
) -> Dict[str, Any]:
    """
    Check if two skills are similar enough to be duplicates.

    Uses simple string similarity based on character overlap.

    Args:
        skill1_name: First skill name
        skill2_name: Second skill name
        threshold: Similarity threshold (0.0 to 1.0)

    Returns:
        Dictionary with is_similar flag and similarity score
    """
    # Normalize names
    name1 = skill1_name.lower().strip()
    name2 = skill2_name.lower().strip()

    # Simple character-based similarity
    # For production, consider using more sophisticated algorithms
    set1 = set(name1)
    set2 = set(name2)

    if not set1 or not set2:
        return {"is_similar": False, "similarity_score": 0.0}

    intersection = len(set1 & set2)
    union = len(set1 | set2)

    similarity = intersection / union if union > 0 else 0.0

    # Also check for substring match
    if name1 in name2 or name2 in name1:
        similarity = max(similarity, 0.9)

    return {
        "is_similar": similarity >= threshold,
        "similarity_score": round(similarity, 3)
    }


def categorize_skill_content(
    skill_description: Annotated[str, Field(description="Skill description text")],
    key_concepts: Annotated[List[str], Field(description="List of key concepts")]
) -> str:
    """
    Suggest a category for a skill based on its content.

    Args:
        skill_description: Description of the skill
        key_concepts: Key concepts associated with the skill

    Returns:
        Suggested category name
    """
    # Combine description and concepts for analysis
    content = f"{skill_description} {' '.join(key_concepts)}".lower()

    # Category keywords
    categories = {
        "Data Manipulation": [
            "pandas", "dataframe", "numpy", "array", "data cleaning",
            "csv", "excel", "data analysis", "filtering", "grouping"
        ],
        "Data Visualization": [
            "matplotlib", "seaborn", "plot", "chart", "graph",
            "visualization", "dash", "plotly"
        ],
        "Web Development": [
            "fastapi", "flask", "django", "http", "api", "rest",
            "web", "server", "endpoint", "route"
        ],
        "Web Scraping": [
            "beautifulsoup", "scraping", "html", "parsing",
            "requests", "selenium", "xpath"
        ],
        "Testing": [
            "pytest", "test", "unittest", "mock", "fixture",
            "tdd", "debugging", "assert"
        ],
        "Automation": [
            "script", "automation", "cli", "command line",
            "file operations", "batch", "workflow"
        ],
        "Clean Code": [
            "refactor", "design pattern", "solid", "clean code",
            "best practices", "code quality", "architecture", "structure",
            "maintainability", "readability", "naming", "functions",
            "classes", "modules", "separation of concerns", "dry", "kiss"
        ],
        "Machine Learning": [
            "scikit-learn", "model", "training", "prediction",
            "classification", "regression", "ml", "neural"
        ],
        "Statistics": [
            "statistics", "probability", "bayesian", "distribution",
            "statistical", "hypothesis"
        ],
        "Algorithms": [
            "algorithm", "sorting", "searching", "tree", "graph",
            "complexity", "optimization"
        ],
        "Data Structures": [
            "list", "dict", "set", "stack", "queue", "linked list",
            "hash table", "data structure"
        ]
    }

    # Score each category
    scores = {}
    for category, keywords in categories.items():
        score = sum(1 for keyword in keywords if keyword in content)
        if score > 0:
            scores[category] = score

    # Return highest scoring category, or default
    if scores:
        return max(scores, key=scores.get)
    else:
        return "General Python"


def generate_skill_markdown(
    skill_data: Annotated[str, Field(description="JSON string of skill data")],
    tracks: Annotated[List[str], Field(description="Learning tracks this skill belongs to")]
) -> str:
    """
    Generate markdown content for a skill file.

    Args:
        skill_data: JSON string containing skill information
        tracks: List of learning track names

    Returns:
        Formatted markdown content
    """
    try:
        skill = json.loads(skill_data)

        # Build markdown content
        lines = [
            f"# {skill.get('name', 'Untitled Skill')}",
            "",
            f"**Tracks**: {', '.join(tracks) if tracks else 'General'}",
            f"**Difficulty**: {skill.get('difficulty', 'unknown')}",
            f"**Category**: {skill.get('category', 'Uncategorized')}",
            "",
            "## Description",
            "",
            skill.get('description', 'No description available.'),
            "",
            "## Key Concepts",
            ""
        ]

        # Add key concepts
        for concept in skill.get('key_concepts', []):
            lines.append(f"- {concept}")

        # Add prerequisites if present
        if 'prerequisites' in skill and skill['prerequisites']:
            lines.extend(["", "## Prerequisites", ""])
            for prereq in skill['prerequisites']:
                prereq_slug = slugify(prereq)
                lines.append(f"- [{prereq}](./{prereq_slug}.md)")

        # Add related skills if present
        if 'related_skills' in skill and skill['related_skills']:
            lines.extend(["", "## Related Skills", ""])
            for related in skill['related_skills']:
                related_slug = slugify(related)
                lines.append(f"- [{related}](./{related_slug}.md)")

        # Add source information
        lines.extend(["", "## Learning Resources", ""])
        source_book = skill.get('source_book', 'Unknown source')
        source_section = skill.get('source_section', 'Unknown section')
        lines.append(f"- **{source_book}**: {source_section}")

        # Footer
        lines.extend(["", "---", "", f"*Source: {source_book}*"])

        return "\n".join(lines)

    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON - {str(e)}"


def slugify(text: Annotated[str, Field(description="Text to convert to URL-friendly slug")]) -> str:
    """
    Convert text to URL-friendly slug.

    Args:
        text: Text to slugify

    Returns:
        Slugified text
    """
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def extract_code_blocks(
    markdown_text: Annotated[str, Field(description="Markdown text to parse")]
) -> List[Dict[str, str]]:
    """
    Extract code blocks from markdown text.

    Args:
        markdown_text: Markdown content

    Returns:
        List of dictionaries with language and code
    """
    # Pattern to match fenced code blocks
    pattern = r'```(\w+)?\n(.*?)```'

    matches = re.findall(pattern, markdown_text, re.DOTALL)

    code_blocks = []
    for language, code in matches:
        code_blocks.append({
            "language": language or "text",
            "code": code.strip()
        })

    return code_blocks


def merge_skill_duplicates(
    skill1_json: Annotated[str, Field(description="First skill as JSON")],
    skill2_json: Annotated[str, Field(description="Second skill as JSON")]
) -> str:
    """
    Merge two similar skills into one, combining their information.

    Args:
        skill1_json: First skill data as JSON string
        skill2_json: Second skill data as JSON string

    Returns:
        Merged skill as JSON string
    """
    try:
        skill1 = json.loads(skill1_json)
        skill2 = json.loads(skill2_json)

        # Start with skill1 as base
        merged = skill1.copy()

        # Merge key_concepts (unique values)
        concepts1 = set(skill1.get('key_concepts', []))
        concepts2 = set(skill2.get('key_concepts', []))
        merged['key_concepts'] = sorted(list(concepts1 | concepts2))

        # Merge prerequisites
        prereqs1 = set(skill1.get('prerequisites', []))
        prereqs2 = set(skill2.get('prerequisites', []))
        merged['prerequisites'] = sorted(list(prereqs1 | prereqs2))

        # Merge related_skills
        related1 = set(skill1.get('related_skills', []))
        related2 = set(skill2.get('related_skills', []))
        merged['related_skills'] = sorted(list(related1 | related2))

        # Use longer description
        desc1 = skill1.get('description', '')
        desc2 = skill2.get('description', '')
        merged['description'] = desc1 if len(desc1) > len(desc2) else desc2

        # Track merged sources
        sources = []
        if 'source_book' in skill1:
            sources.append(skill1['source_book'])
        if 'source_book' in skill2 and skill2['source_book'] not in sources:
            sources.append(skill2['source_book'])

        merged['merged_from'] = sources

        return json.dumps(merged, indent=2)

    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {str(e)}"})


# Tool registry for easy access
AVAILABLE_TOOLS = [
    extract_pdf_text,
    chunk_content,
    validate_skill_structure,
    check_skill_similarity,
    categorize_skill_content,
    generate_skill_markdown,
    slugify,
    extract_code_blocks,
    merge_skill_duplicates
]


def get_tool_by_name(name: str):
    """Get a tool function by name"""
    for tool in AVAILABLE_TOOLS:
        if tool.__name__ == name:
            return tool
    return None
