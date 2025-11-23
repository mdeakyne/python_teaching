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
    assert len(filtered) == 2
    assert all(s["category"] in ["portfolio_analysis", "risk_metrics"] for s in filtered)
