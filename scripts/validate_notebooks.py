#!/usr/bin/env python3
"""Validate generated notebooks by executing them."""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def execute_notebook(notebook_path: Path) -> tuple[bool, str]:
    """Execute a notebook and return success status.

    Args:
        notebook_path: Path to .ipynb file

    Returns:
        Tuple of (success: bool, error_message: str)
    """
    try:
        # Use nbconvert to execute
        result = subprocess.run(
            [
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "--output",
                str(notebook_path.name),
                "--output-dir",
                str(notebook_path.parent),
                str(notebook_path),
            ],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )

        if result.returncode == 0:
            return True, ""
        else:
            return False, result.stderr

    except subprocess.TimeoutExpired:
        return False, "Execution timeout (5 minutes)"
    except Exception as e:
        return False, str(e)


def validate_notebook_structure(notebook_path: Path) -> tuple[bool, str]:
    """Validate notebook JSON structure.

    Args:
        notebook_path: Path to .ipynb file

    Returns:
        Tuple of (valid: bool, error_message: str)
    """
    try:
        notebook = json.loads(notebook_path.read_text())

        # Check required fields
        if "cells" not in notebook:
            return False, "Missing 'cells' field"

        if "metadata" not in notebook:
            return False, "Missing 'metadata' field"

        if "nbformat" not in notebook:
            return False, "Missing 'nbformat' field"

        # Check cells
        if len(notebook["cells"]) == 0:
            return False, "No cells in notebook"

        for i, cell in enumerate(notebook["cells"]):
            if "cell_type" not in cell:
                return False, f"Cell {i} missing 'cell_type'"

            if "source" not in cell:
                return False, f"Cell {i} missing 'source'"

        return True, ""

    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description="Validate generated notebooks")
    parser.add_argument(
        "--notebook-dir",
        type=str,
        default="../demos/interview_prep",
        help="Directory containing notebooks to validate",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute notebooks to verify they run (slow)",
    )

    args = parser.parse_args()

    notebook_dir = Path(args.notebook_dir)
    if not notebook_dir.exists():
        print(f"Error: Directory not found: {notebook_dir}")
        return 1

    notebooks = list(notebook_dir.glob("*.ipynb"))
    if not notebooks:
        print(f"No notebooks found in {notebook_dir}")
        return 1

    print(f"Validating {len(notebooks)} notebooks...\n")

    results = []

    for notebook_path in notebooks:
        print(f"Checking {notebook_path.name}...")

        # Step 1: Validate structure
        valid, error = validate_notebook_structure(notebook_path)
        if not valid:
            print(f"  ✗ INVALID STRUCTURE: {error}")
            results.append((notebook_path.name, False, error))
            continue

        print(f"  ✓ Valid structure")

        # Step 2: Execute if requested
        if args.execute:
            print(f"  Executing (may take a minute)...")
            success, error = execute_notebook(notebook_path)

            if success:
                print(f"  ✓ Executed successfully")
                results.append((notebook_path.name, True, ""))
            else:
                print(f"  ✗ EXECUTION FAILED: {error[:100]}")
                results.append((notebook_path.name, False, error))
        else:
            results.append((notebook_path.name, True, ""))

    # Summary
    print(f"\n{'=' * 60}")
    print("VALIDATION SUMMARY")
    print(f"{'=' * 60}")

    passed = sum(1 for _, success, _ in results if success)
    failed = len(results) - passed

    print(f"Total: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed > 0:
        print(f"\nFailed notebooks:")
        for name, success, error in results:
            if not success:
                print(f"  - {name}: {error[:80]}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
