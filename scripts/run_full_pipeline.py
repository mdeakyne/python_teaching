#!/usr/bin/env python3
"""Run the complete skill extraction and notebook generation pipeline."""

import argparse
import sys
from pathlib import Path
from datetime import datetime


def run_command(cmd: str, description: str) -> bool:
    """Run a command and print status.

    Args:
        cmd: Command to run
        description: Description for user

    Returns:
        True if successful, False otherwise
    """
    import subprocess

    print(f"\n{'=' * 60}")
    print(f"STEP: {description}")
    print(f"{'=' * 60}")

    result = subprocess.run(cmd, shell=True)

    if result.returncode == 0:
        print(f"✓ {description} completed")
        return True
    else:
        print(f"✗ {description} failed")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run full pipeline")
    parser.add_argument(
        "--pdfs", type=str, help="Comma-separated PDF names (or 'all' for all PDFs)"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Number of notebooks to generate (default: 5)",
    )
    parser.add_argument(
        "--skip-extraction",
        action="store_true",
        help="Skip skill extraction (use existing taxonomy)",
    )
    parser.add_argument(
        "--skip-validation", action="store_true", help="Skip notebook validation"
    )

    args = parser.parse_args()

    start_time = datetime.now()

    print("""
╔══════════════════════════════════════════════════════════╗
║   Financial Demo Skill Extraction & Generation Pipeline  ║
╚══════════════════════════════════════════════════════════╝
""")

    # Step 1: List PDFs if needed
    if args.pdfs == "all":
        if not run_command(
            "python extract_skills_taxonomy.py --list-new | tail -n +2 | head -n -2 | cut -d'-' -f2- | tr '\n' ',' > /tmp/pdfs.txt",
            "List all PDFs",
        ):
            return 1

        with open("/tmp/pdfs.txt") as f:
            args.pdfs = f.read().strip().rstrip(",")

    if not args.pdfs:
        print("Error: --pdfs required (use 'all' for all PDFs or comma-separated list)")
        return 1

    # Step 2: Extract skills
    if not args.skip_extraction:
        if not run_command(
            f'python extract_skills_taxonomy.py --pdfs "{args.pdfs}" --model chat',
            "Extract skills from PDFs",
        ):
            return 1

    # Step 3: Filter financial skills
    if not run_command(
        "python filter_financial_skills.py --threshold 8 --categories portfolio_analysis,risk_metrics,time_series,visualization",
        "Filter financial-focused skills",
    ):
        return 1

    # Step 4: Generate notebooks
    if not run_command(
        f"python generate_demo_notebooks.py --count {args.count} --model mini",
        f"Generate {args.count} demo notebooks",
    ):
        return 1

    # Step 5: Validate notebooks
    if not args.skip_validation:
        if not run_command(
            "python validate_notebooks.py --notebook-dir ../demos/interview_prep",
            "Validate generated notebooks",
        ):
            print("\nWarning: Validation failed, but notebooks were generated")

    # Done
    duration = datetime.now() - start_time

    print(f"""
{"=" * 60}
✓ PIPELINE COMPLETE
{"=" * 60}

Duration: {duration}

Generated notebooks are in: demos/interview_prep/

To view:
  cd ../demos/interview_prep
  jupyter lab

Next steps:
  1. Review generated notebooks
  2. Test execute each notebook
  3. Customize narratives if needed
  4. Practice presenting demos
""")

    return 0


if __name__ == "__main__":
    sys.exit(main())
