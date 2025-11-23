import os
import tempfile
from pathlib import Path

import pytest


def test_list_new_pdfs():
    """Test listing PDFs from references directory"""
    from pdf_converter import list_pdfs

    pdfs = list_pdfs("../../../references")

    assert isinstance(pdfs, list)
    assert len(pdfs) > 0
    assert all(pdf.endswith(".pdf") for pdf in pdfs)
    assert "Financial Data Engineering.pdf" in pdfs


def test_convert_pdf_to_markdown():
    """Test PDF conversion to markdown"""
    from pdf_converter import convert_pdf_to_markdown

    # Use a small test PDF (we'll use one of the existing ones)
    pdf_path = "../../../references/Dive Into Data Science.pdf"

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_output.md"

        result = convert_pdf_to_markdown(pdf_path, output_path)

        assert result is True
        assert output_path.exists()
        assert output_path.stat().st_size > 0

        # Check content
        content = output_path.read_text()
        assert len(content) > 100
        assert "# " in content  # Has markdown headers
