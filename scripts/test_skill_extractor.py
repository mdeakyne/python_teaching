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
    )

    # Convert to dict
    skill_dict = skill.to_dict()

    assert skill_dict["skill_id"] == "test_001"
    assert skill_dict["financial_relevance"] == 8
    assert "pandas" in skill_dict["prerequisites"]
