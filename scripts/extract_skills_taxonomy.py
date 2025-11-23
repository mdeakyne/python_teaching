#!/usr/bin/env python3
"""Extract skills from PDFs and build taxonomy."""

import argparse
import sys
from datetime import date
from pathlib import Path

from pdf_converter import convert_pdf_to_markdown, list_pdfs
from skill_extractor import extract_skills_from_markdown, save_skills_to_json


def main():
    parser = argparse.ArgumentParser(description="Extract skills from PDFs")
    parser.add_argument(
        "--pdfs",
        type=str,
        help="Comma-separated list of PDF filenames (if not provided, lists available PDFs)",
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        default="../references",
        help="Directory containing PDFs (default: ../references)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="../references/_skill_taxonomy",
        help="Output directory for skill taxonomy (default: ../references/_skill_taxonomy)",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["chat", "mini"],
        default="chat",
        help="Azure OpenAI model to use (default: chat)",
    )
    parser.add_argument(
        "--list-new", action="store_true", help="List all available PDFs and exit"
    )

    args = parser.parse_args()

    # List PDFs if requested
    if args.list_new:
        print("Available PDFs:")
        pdfs = list_pdfs(args.input_dir)
        for pdf in pdfs:
            print(f"  - {pdf}")
        print(f"\nTotal: {len(pdfs)} PDFs")
        return 0

    # Validate input
    if not args.pdfs:
        print("Error: --pdfs required (or use --list-new to see available PDFs)")
        return 1

    pdf_names = [p.strip() for p in args.pdfs.split(",")]

    # Create output directories
    markdown_dir = Path("../references/_markdown")
    markdown_dir.mkdir(parents=True, exist_ok=True)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each PDF
    extraction_date = date.today().isoformat()

    for pdf_name in pdf_names:
        print(f"\n{'=' * 60}")
        print(f"Processing: {pdf_name}")
        print(f"{'=' * 60}")

        # Step 1: Convert to markdown
        print("Step 1: Converting to markdown...")
        md_name = pdf_name.replace(".pdf", ".md")
        md_path = markdown_dir / md_name

        pdf_path = Path(args.input_dir) / pdf_name
        if not pdf_path.exists():
            print(f"  ERROR: PDF not found: {pdf_path}")
            continue

        success = convert_pdf_to_markdown(str(pdf_path), str(md_path))
        if not success:
            print(f"  ERROR: Failed to convert {pdf_name}")
            continue

        print(f"  ✓ Markdown saved to {md_path}")

        # Step 2: Extract skills
        print("Step 2: Extracting skills with LLM...")
        markdown_content = md_path.read_text()

        book_title = pdf_name.replace(".pdf", "").replace("_", " ")

        skills = extract_skills_from_markdown(
            markdown_content, book_title=book_title, use_llm=True, model=args.model
        )

        print(f"  ✓ Extracted {len(skills)} skills")

        # Step 3: Save to JSON
        print("Step 3: Saving skill taxonomy...")
        json_name = pdf_name.replace(".pdf", "_skills.json")
        json_path = output_dir / json_name

        save_skills_to_json(skills, str(json_path), book_title, extraction_date)
        print(f"  ✓ Saved to {json_path}")

        # Print summary
        categories = {}
        for skill in skills:
            cat = skill.category
            categories[cat] = categories.get(cat, 0) + 1

        print(f"\n  Summary:")
        for cat, count in sorted(categories.items()):
            print(f"    {cat}: {count} skills")

    print(f"\n{'=' * 60}")
    print("✓ All PDFs processed successfully")
    print(f"{'=' * 60}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
