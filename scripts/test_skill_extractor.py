import json
import tempfile
from pathlib import Path

import pytest


def test_extract_skills_from_markdown():
    """Test skill extraction from markdown content"""
    from skill_extractor import extract_skills_from_markdown

    sample_markdown = """
    ## Chapter 3: Portfolio Performance Metrics

    In this chapter, we'll learn how to calculate time-weighted returns (TWR)
    and money-weighted returns (MWR) using pandas. These are essential metrics
    for evaluating portfolio performance.

    ### Calculating Returns

    We'll use daily price data to compute returns with pandas.
    """

    skills = extract_skills_from_markdown(
        sample_markdown,
        book_title="Test Book",
        use_llm=False,  # Use rule-based extraction for testing
    )

    assert isinstance(skills, list)
    # Rule-based should find at least the chapter as a skill
    assert len(skills) > 0


def test_skill_json_schema():
    """Test that extracted skills match expected schema"""
    from skill_extractor import Skill

    skill = Skill(
        skill_id="test_001",
        skill_name="Test Skill",
        category="portfolio_analysis",
        subcategory="returns",
        description="A test skill",
        source_chapter="Chapter 1",
        difficulty="intermediate",
        prerequisites=["pandas"],
        financial_relevance=8,
        keywords=["test"],
        example_context="Example text",
        tracks=["financial-analytics"],
        key_concepts=["returns", "performance"],
        learning_resources=["**test-book**: Chapter 1"],
    )

    # Convert to dict
    skill_dict = skill.to_dict()

    assert skill_dict["skill_id"] == "test_001"
    assert skill_dict["financial_relevance"] == 8
    assert "pandas" in skill_dict["prerequisites"]
    assert "financial-analytics" in skill_dict["tracks"]
    assert "returns" in skill_dict["key_concepts"]


def test_skill_to_markdown():
    """Test that skills can be converted to markdown format"""
    from skill_extractor import Skill

    skill = Skill(
        skill_id="test_001",
        skill_name="Test Skill",
        category="portfolio_analysis",
        subcategory="returns",
        description="A test skill for markdown generation",
        source_chapter="Chapter 1: Introduction",
        difficulty="intermediate",
        prerequisites=["pandas basics", "numpy"],
        financial_relevance=8,
        keywords=["test"],
        example_context="Example text",
        tracks=["financial-analytics", "data-science"],
        key_concepts=["returns", "performance", "metrics"],
        learning_resources=["**test-book**: Chapter 1: Introduction"],
    )

    # Generate markdown
    markdown = skill.to_markdown(book_name="test-book")

    # Verify markdown structure
    assert "# Test Skill" in markdown
    assert "**Tracks**: financial-analytics, data-science" in markdown
    assert "**Difficulty**: intermediate" in markdown
    assert "**Category**: portfolio_analysis" in markdown
    assert "## Description" in markdown
    assert "A test skill for markdown generation" in markdown
    assert "## Key Concepts" in markdown
    assert "- returns" in markdown
    assert "- performance" in markdown
    assert "## Prerequisites" in markdown
    assert "[pandas basics](./pandas-basics.md)" in markdown
    assert "## Learning Resources" in markdown
    assert "*Source: test-book*" in markdown


def test_save_skills_to_markdown():
    """Test saving skills to markdown files"""
    from skill_extractor import Skill, save_skills_to_markdown

    skill = Skill(
        skill_id="test_001",
        skill_name="Test Portfolio Skill",
        category="portfolio_analysis",
        subcategory="returns",
        description="A test skill",
        source_chapter="Chapter 1",
        difficulty="intermediate",
        prerequisites=["pandas"],
        financial_relevance=8,
        keywords=["test"],
        example_context="Example text",
        tracks=["financial-analytics"],
        key_concepts=["returns"],
        learning_resources=["**test-book**: Chapter 1"],
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        save_skills_to_markdown([skill], tmpdir, "Test Book")

        # Check file was created
        expected_file = Path(tmpdir) / "test-portfolio-skill.md"
        assert expected_file.exists()

        # Verify content
        content = expected_file.read_text()
        assert "# Test Portfolio Skill" in content
        assert "**Difficulty**: intermediate" in content
