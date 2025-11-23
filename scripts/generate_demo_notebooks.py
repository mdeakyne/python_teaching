#!/usr/bin/env python3
"""Generate demo Jupyter notebooks from filtered skills."""

import argparse
import json
from pathlib import Path
import sys

from notebook_generator import generate_multiple_notebooks


def main():
    parser = argparse.ArgumentParser(description="Generate demo notebooks from skills")
    parser.add_argument(
        "--skills-file",
        type=str,
        default="../references/_skill_taxonomy/finance_focused_skills.json",
        help="Path to filtered skills JSON file",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Number of notebooks to generate (default: 5)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="../demos/interview_prep",
        help="Output directory for notebooks",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["chat", "mini"],
        default="mini",
        help="Azure OpenAI model to use (default: mini)",
    )
    parser.add_argument(
        "--interactive", action="store_true", help="Interactively select skills"
    )

    args = parser.parse_args()

    # Load skills
    skills_file = Path(args.skills_file)
    if not skills_file.exists():
        print(f"Error: Skills file not found: {skills_file}")
        print("Run extract_skills_taxonomy.py and filter_financial_skills.py first")
        return 1

    data = json.loads(skills_file.read_text())
    all_skills = data.get("skills", [])

    print(f"Loaded {len(all_skills)} skills from {skills_file}")

    # Select skills
    if args.interactive:
        print("\nTop skills:")
        for i, skill in enumerate(all_skills[:20], 1):
            print(
                f"  {i}. {skill['skill_name']} ({skill['category']}, relevance: {skill['financial_relevance']})"
            )

        print(f"\nEnter skill numbers to generate (comma-separated, max {args.count}):")
        selection = input("> ").strip()

        indices = [int(x.strip()) - 1 for x in selection.split(",")]
        selected_skills = [all_skills[i] for i in indices if 0 <= i < len(all_skills)]
    else:
        # Take top N skills
        selected_skills = all_skills[: args.count]

    print(f"\nGenerating {len(selected_skills)} notebooks:")
    for i, skill in enumerate(selected_skills, 1):
        print(f"  {i}. {skill['skill_name']}")

    # Generate notebooks
    print(f"\n{'=' * 60}")
    print("Starting generation...")
    print(f"{'=' * 60}")

    notebook_paths = generate_multiple_notebooks(
        selected_skills, output_dir=args.output, model=args.model
    )

    print(f"\n{'=' * 60}")
    print(f"✓ Generated {len(notebook_paths)} notebooks")
    print(f"{'=' * 60}")
    print(f"\nNotebooks saved to: {args.output}")
    for path in notebook_paths:
        print(f"  - {Path(path).name}")

    print(f"\nTo view: cd {args.output} && jupyter lab")

    return 0


if __name__ == "__main__":
    sys.exit(main())
