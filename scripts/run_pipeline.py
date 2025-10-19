#!/usr/bin/env python3
"""
Convenience script to run the full PDF-to-Skills pipeline

Usage:
    python scripts/run_pipeline.py                    # Run all steps
    python scripts/run_pipeline.py --step 1           # Run only PDF conversion
    python scripts/run_pipeline.py --step 2           # Run only skill extraction
    python scripts/run_pipeline.py --step 3           # Run only organization
    python scripts/run_pipeline.py --books "book1" "book2"  # Process specific books
"""

import subprocess
import sys
from pathlib import Path
import argparse

from rich.console import Console
from rich.panel import Panel


console = Console()


def run_command(command: list, description: str) -> bool:
    """Run a command and return success status"""
    console.print(Panel(description, style="bold cyan"))

    try:
        result = subprocess.run(
            command,
            cwd=Path(__file__).parent.parent,
            check=True
        )
        console.print(f"[green]✓ {description} completed successfully[/green]\n")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]✗ {description} failed with error code {e.returncode}[/red]\n")
        return False
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run PDF-to-Skills pipeline")
    parser.add_argument(
        "--step",
        type=int,
        choices=[1, 2, 3],
        help="Run only a specific step (1=PDF→MD, 2=Extract, 3=Organize)"
    )
    parser.add_argument(
        "--books",
        nargs="+",
        help="Specific books to process (for step 1)"
    )

    args = parser.parse_args()

    console.print("[bold magenta]PDF-to-Skills Processing Pipeline[/bold magenta]\n")

    steps = []

    if args.step is None or args.step == 1:
        # Step 1: PDF to Markdown
        cmd = ["uv", "run", "python", "scripts/pdf_to_markdown.py"]
        if args.books:
            cmd.extend(args.books)
        steps.append((cmd, "Step 1: PDF → Markdown Conversion"))

    if args.step is None or args.step == 2:
        # Step 2: Extract Skills
        steps.append((
            ["uv", "run", "python", "scripts/extract_skills.py"],
            "Step 2: Skill Extraction"
        ))

    if args.step is None or args.step == 3:
        # Step 3: Organize & Map
        steps.append((
            ["uv", "run", "python", "scripts/organize_skills.py"],
            "Step 3: Organize & Map to Tracks"
        ))

    # Run each step
    for i, (cmd, description) in enumerate(steps, 1):
        success = run_command(cmd, description)

        if not success:
            console.print(f"[red]Pipeline stopped at step {i}[/red]")
            sys.exit(1)

        if i < len(steps):
            console.print("[cyan]" + "="*60 + "[/cyan]\n")

    # Success!
    console.print(Panel.fit(
        "[bold green]✓ Pipeline completed successfully![/bold green]\n\n"
        "Generated skills are in: skills/\n"
        "View the master catalog: skills/index.md",
        title="Success",
        border_style="green"
    ))


if __name__ == "__main__":
    main()
