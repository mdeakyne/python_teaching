"""PDF to Markdown conversion utilities."""

import re
from pathlib import Path
from typing import List

import pdfplumber


def list_pdfs(directory: str) -> List[str]:
    """List all PDF files in directory.

    Args:
        directory: Path to directory containing PDFs

    Returns:
        List of PDF filenames (not full paths)
    """
    pdf_dir = Path(directory)
    if not pdf_dir.exists():
        raise ValueError(f"Directory not found: {directory}")

    pdfs = [p.name for p in pdf_dir.glob("*.pdf")]
    return sorted(pdfs)


def convert_pdf_to_markdown(pdf_path: str, output_path: str) -> bool:
    """Convert PDF to markdown format.

    Args:
        pdf_path: Path to input PDF file
        output_path: Path to output markdown file

    Returns:
        True if conversion successful, False otherwise
    """
    try:
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            raise ValueError(f"PDF not found: {pdf_path}")

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        markdown_lines = []

        with pdfplumber.open(pdf_file) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    # Basic markdown formatting
                    # Detect chapter headers (usually all caps or starts with "Chapter")
                    lines = text.split("\n")
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue

                        # Chapter headers
                        if re.match(r"^(CHAPTER|Chapter)\s+\d+", line):
                            markdown_lines.append(f"\n## {line}\n")
                        # Section headers (heuristic: short lines in title case)
                        elif (
                            len(line) < 80
                            and line[0].isupper()
                            and not line.endswith(".")
                        ):
                            markdown_lines.append(f"\n### {line}\n")
                        else:
                            markdown_lines.append(line)

                    markdown_lines.append(f"\n---\n*Page {page_num}*\n")

        # Write to file
        output_file.write_text("\n".join(markdown_lines))
        return True

    except Exception as e:
        print(f"Error converting PDF: {e}")
        return False


def convert_multiple_pdfs(
    pdf_names: List[str], input_dir: str, output_dir: str
) -> dict:
    """Convert multiple PDFs to markdown.

    Args:
        pdf_names: List of PDF filenames
        input_dir: Directory containing PDFs
        output_dir: Directory for markdown output

    Returns:
        Dict mapping PDF name to conversion status (True/False)
    """
    results = {}

    for pdf_name in pdf_names:
        pdf_path = Path(input_dir) / pdf_name
        output_name = pdf_name.replace(".pdf", ".md")
        output_path = Path(output_dir) / output_name

        print(f"Converting {pdf_name}...")
        results[pdf_name] = convert_pdf_to_markdown(str(pdf_path), str(output_path))

    return results
