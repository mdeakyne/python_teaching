import json
import tempfile
from pathlib import Path

import pytest


def test_filter_skills_by_relevance():
    """Test filtering skills by financial relevance"""
    from filter_financial_skills import filter_by_relevance

    skills = [
        {"skill_name": "Portfolio Returns", "financial_relevance": 10},
        {"skill_name": "Web Scraping", "financial_relevance": 2},
        {"skill_name": "Risk Metrics", "financial_relevance": 9},
    ]

    filtered = filter_by_relevance(skills, threshold=8)

    assert len(filtered) == 2
    assert filtered[0]["skill_name"] in ["Portfolio Returns", "Risk Metrics"]


def test_filter_skills_by_category():
    """Test filtering skills by category"""
    from filter_financial_skills import filter_by_category

    skills = [
        {"skill_name": "Portfolio Returns", "category": "portfolio_analysis"},
        {"skill_name": "Data Cleaning", "category": "data_cleaning"},
        {"skill_name": "VaR Calculation", "category": "risk_metrics"},
    ]

    filtered = filter_by_category(
        skills, categories=["portfolio_analysis", "risk_metrics"]
    )

    assert len(filtered) == 2
    assert all(
        s["category"] in ["portfolio_analysis", "risk_metrics"] for s in filtered
    )


def test_parse_markdown_skill():
    """Test parsing a markdown skill file"""
    from filter_financial_skills import parse_markdown_skill

    # Create a sample markdown file
    sample_markdown = """# Time-Weighted Return Calculation

**Tracks**: financial-analytics, data-science
**Difficulty**: intermediate
**Category**: Portfolio Analysis

## Description

Calculate time-weighted returns to measure portfolio performance independent of cash flows.

## Key Concepts

- time-weighted returns
- geometric linking
- cash flow independence
- pandas aggregation

## Prerequisites

- [pandas basics](./pandas-basics.md)
- [datetime handling](./datetime-handling.md)

## Learning Resources

- **financial-python**: Chapter 3: Portfolio Metrics

---

*Source: financial-python*
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        md_path = Path(tmpdir) / "time-weighted-return-calculation.md"
        md_path.write_text(sample_markdown)

        skill = parse_markdown_skill(md_path)

        assert skill["skill_name"] == "Time-Weighted Return Calculation"
        assert skill["difficulty"] == "intermediate"
        assert skill["category"] == "Portfolio Analysis"
        assert "financial-analytics" in skill["tracks"]
        assert "data-science" in skill["tracks"]
        assert "time-weighted returns" in skill["key_concepts"]
        assert "geometric linking" in skill["key_concepts"]
        assert skill["source"] == "financial-python"
        assert skill["financial_relevance"] == 10  # Portfolio Analysis = 10


def test_parse_markdown_minimal():
    """Test parsing a minimal markdown skill file"""
    from filter_financial_skills import parse_markdown_skill

    minimal_markdown = """# Basic Skill

**Tracks**: financial-analytics
**Difficulty**: beginner
**Category**: data_cleaning

## Description

A basic skill with minimal information.

---

*Source: test-book*
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        md_path = Path(tmpdir) / "basic-skill.md"
        md_path.write_text(minimal_markdown)

        skill = parse_markdown_skill(md_path)

        assert skill["skill_name"] == "Basic Skill"
        assert skill["difficulty"] == "beginner"
        assert skill["category"] == "data_cleaning"
        assert skill["financial_relevance"] == 6  # data_cleaning = 6
        assert len(skill["key_concepts"]) == 0
