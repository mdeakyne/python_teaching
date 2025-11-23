#!/usr/bin/env python3
"""Filter and prioritize financial skills from taxonomy."""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List


def parse_markdown_skill(md_path: Path) -> Dict:
    """Parse a markdown skill file into a dictionary.

    Args:
        md_path: Path to markdown file

    Returns:
        Dictionary with skill metadata
    """
    content = md_path.read_text()

    # Extract title (first # heading)
    title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
    skill_name = title_match.group(1) if title_match else md_path.stem

    # Extract tracks
    tracks_match = re.search(r"\*\*Tracks\*\*: (.+)$", content, re.MULTILINE)
    tracks = (
        [t.strip() for t in tracks_match.group(1).split(",")] if tracks_match else []
    )

    # Extract difficulty
    difficulty_match = re.search(r"\*\*Difficulty\*\*: (\w+)", content)
    difficulty = difficulty_match.group(1) if difficulty_match else "intermediate"

    # Extract category
    category_match = re.search(r"\*\*Category\*\*: (.+)$", content, re.MULTILINE)
    category = category_match.group(1).strip() if category_match else "unknown"

    # Extract description (first paragraph after ## Description)
    desc_match = re.search(r"## Description\s+(.+?)(?=\n\n|\n##)", content, re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else ""

    # Extract source
    source_match = re.search(r"\*Source: (.+?)\*", content)
    source = source_match.group(1) if source_match else "unknown"

    # Extract key concepts
    key_concepts = []
    concepts_section = re.search(
        r"## Key Concepts\s+(.+?)(?=\n##|\n---)", content, re.DOTALL
    )
    if concepts_section:
        concepts_text = concepts_section.group(1)
        key_concepts = [
            line.strip("- ").strip()
            for line in concepts_text.split("\n")
            if line.strip().startswith("-")
        ]

    # Map category to financial relevance score (heuristic)
    relevance_map = {
        "portfolio_analysis": 10,
        "Portfolio Analysis": 10,
        "risk_metrics": 10,
        "Risk Metrics": 10,
        "time_series": 9,
        "Time Series": 9,
        "statistical_methods": 8,
        "Statistical Methods": 8,
        "visualization": 7,
        "Visualization": 7,
        "data_cleaning": 6,
        "Data Cleaning": 6,
    }

    financial_relevance = relevance_map.get(category, 5)

    return {
        "skill_name": skill_name,
        "category": category,
        "difficulty": difficulty,
        "description": description,
        "tracks": tracks,
        "key_concepts": key_concepts,
        "source": source,
        "financial_relevance": financial_relevance,
        "file_path": str(md_path),
    }


def filter_by_relevance(skills: List[Dict], threshold: int = 8) -> List[Dict]:
    """Filter skills by financial relevance score.

    Args:
        skills: List of skill dictionaries
        threshold: Minimum financial_relevance score (default: 8)

    Returns:
        Filtered list of skills
    """
    return [s for s in skills if s.get("financial_relevance", 0) >= threshold]


def filter_by_category(skills: List[Dict], categories: List[str]) -> List[Dict]:
    """Filter skills by category.

    Args:
        skills: List of skill dictionaries
        categories: List of allowed categories

    Returns:
        Filtered list of skills
    """
    return [s for s in skills if s.get("category") in categories]


def rank_skills(skills: List[Dict]) -> List[Dict]:
    """Rank skills by financial relevance and difficulty.

    Args:
        skills: List of skill dictionaries

    Returns:
        Sorted list of skills (highest priority first)
    """
    difficulty_score = {"beginner": 1, "intermediate": 2, "advanced": 3}

    def score(skill):
        # Prioritize high financial relevance
        relevance = skill.get("financial_relevance", 0)
        # Slightly prefer intermediate difficulty
        diff = difficulty_score.get(skill.get("difficulty", "intermediate"), 2)
        diff_bonus = 1 if diff == 2 else 0

        return (relevance * 10) + diff_bonus

    return sorted(skills, key=score, reverse=True)


def main():
    parser = argparse.ArgumentParser(
        description="Filter financial skills from taxonomy"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="../references/_skill_taxonomy",
        help="Directory containing skill taxonomy JSON files",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=8,
        help="Minimum financial relevance score (default: 8)",
    )
    parser.add_argument(
        "--categories",
        type=str,
        default="portfolio_analysis,risk_metrics,time_series,visualization",
        help="Comma-separated list of categories to include",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="../references/_skill_taxonomy/finance_focused_skills.json",
        help="Output JSON file for filtered skills",
    )

    args = parser.parse_args()

    # Load all skill files
    input_dir = Path(args.input)
    all_skills = []

    print("Loading skill markdown files...")

    # First try loading from markdown files
    skills_dir = input_dir / "financial-analytics"
    if skills_dir.exists():
        for md_file in skills_dir.glob("*.md"):
            print(f"  - {md_file.name}")
            skill = parse_markdown_skill(md_file)
            all_skills.append(skill)

    # Fallback to JSON files if no markdown found
    if not all_skills:
        print("No markdown files found, trying JSON files...")
        for json_file in input_dir.glob("*_skills.json"):
            print(f"  - {json_file.name}")
            data = json.loads(json_file.read_text())

            # Add book_title to each skill
            book_title = data.get("book_title", "Unknown")
            for skill in data.get("skills", []):
                skill["book_source"] = book_title
                all_skills.append(skill)

    print(f"\nTotal skills loaded: {len(all_skills)}")

    # Filter by relevance
    print(f"\nFiltering by financial_relevance >= {args.threshold}...")
    filtered = filter_by_relevance(all_skills, threshold=args.threshold)
    print(f"  ✓ {len(filtered)} skills passed relevance filter")

    # Filter by category
    categories = [c.strip() for c in args.categories.split(",")]
    print(f"\nFiltering by categories: {', '.join(categories)}...")
    filtered = filter_by_category(filtered, categories)
    print(f"  ✓ {len(filtered)} skills passed category filter")

    # Rank skills
    print("\nRanking skills by priority...")
    ranked = rank_skills(filtered)
    print(f"  ✓ Skills ranked")

    # Save output (JSON)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_data = {
        "filter_criteria": {
            "financial_relevance_threshold": args.threshold,
            "categories": categories,
        },
        "total_skills": len(ranked),
        "skills": ranked,
    }

    output_path.write_text(json.dumps(output_data, indent=2))
    print(f"\n✓ Filtered skills saved to: {output_path}")

    # Also generate a markdown index
    md_index_path = output_path.parent / "financial-analytics" / "README.md"
    md_index_path.parent.mkdir(parents=True, exist_ok=True)

    md_lines = [
        "# Financial Analytics Skills",
        "",
        f"**Total Skills**: {len(ranked)}",
        f"**Relevance Threshold**: {args.threshold}",
        f"**Categories**: {', '.join(categories)}",
        "",
        "## Top Skills by Relevance",
        "",
    ]

    for skill in ranked[:20]:  # Top 20
        skill_slug = (
            skill["skill_name"]
            .lower()
            .replace(" ", "-")
            .replace("/", "-")
            .replace("(", "")
            .replace(")", "")
            .replace(":", "")
        )
        md_lines.append(
            f"- [{skill['skill_name']}](./{skill_slug}.md) - {skill['difficulty']} ({skill['category']})"
        )

    md_index_path.write_text("\n".join(md_lines))
    print(f"✓ Markdown index saved to: {md_index_path}")

    # Summary
    print(f"\nTop 10 Skills:")
    for i, skill in enumerate(ranked[:10], 1):
        print(
            f"  {i}. {skill['skill_name']} (relevance: {skill['financial_relevance']}, {skill['difficulty']})"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
