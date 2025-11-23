#!/usr/bin/env python3
"""Filter and prioritize financial skills from taxonomy."""

import argparse
import json
from pathlib import Path
from typing import List, Dict
import sys


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

    print("Loading skill taxonomy files...")
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

    # Save output
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

    # Summary
    print(f"\nTop 10 Skills:")
    for i, skill in enumerate(ranked[:10], 1):
        print(
            f"  {i}. {skill['skill_name']} (relevance: {skill['financial_relevance']}, {skill['difficulty']})"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
