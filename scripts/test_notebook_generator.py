import json
import tempfile
from pathlib import Path

import pytest


def test_generate_notebook_structure():
    """Test notebook generation creates valid structure"""
    from notebook_generator import generate_notebook

    skill = {
        "skill_name": "Portfolio Returns",
        "description": "Calculate portfolio returns",
        "category": "portfolio_analysis",
        "difficulty": "intermediate",
    }

    notebook = generate_notebook(skill, use_llm=False)

    assert "cells" in notebook
    assert len(notebook["cells"]) > 0
    assert notebook["cells"][0]["cell_type"] == "markdown"


def test_save_notebook():
    """Test saving notebook to file"""
    from notebook_generator import save_notebook

    notebook = {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": ["# Test"]},
            {
                "cell_type": "code",
                "metadata": {},
                "source": ["print('hello')"],
                "outputs": [],
                "execution_count": None,
            },
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test.ipynb"
        save_notebook(notebook, str(output_path))

        assert output_path.exists()

        # Verify it's valid JSON
        loaded = json.loads(output_path.read_text())
        assert "cells" in loaded
