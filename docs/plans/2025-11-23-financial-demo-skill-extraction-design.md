# Financial Demo: PDF Skill Extraction & Notebook Generation

**Date:** 2025-11-23  
**Purpose:** Interview prep for managed services role at financial management firm  
**Deliverable:** 3-5 Jupyter notebooks demonstrating portfolio, investment, and risk analytics skills

---

## Executive Summary

This design outlines a system to:
1. Extract exhaustive skill taxonomy from new data science PDFs
2. Generate demo Jupyter notebooks showcasing financial analytics skills
3. Use Azure OpenAI (gpt-5-chat, gpt-5-mini) for automated extraction and generation

**Timeline:** 1-2 days for complete implementation and demo generation

---

## Requirements

### Functional Requirements
- Parse new PDFs added today (26 data science books in `/references`)
- Extract technical skills with metadata (category, difficulty, financial relevance)
- Create structured skill taxonomy (JSON format)
- Generate 3-5 Jupyter notebooks with:
  - Professional narrative explanations
  - Synthetic financial data (portfolios, stocks, risk metrics)
  - Working code (pandas, numpy, matplotlib, seaborn, plotly)
  - Visualizations and business insights

### Domain Focus
- **Portfolio analysis:** returns, attribution, optimization, rebalancing
- **Investment analytics:** performance metrics, asset allocation
- **Risk metrics:** VaR, CVaR, volatility, Sharpe ratio, drawdown, beta

### Non-Functional Requirements
- Notebooks must execute without errors
- Code follows best practices (interview-ready quality)
- Synthetic data is realistic (252 trading days, 8-12% returns, 15-25% volatility)
- Professional tone suitable for financial services context

---

## Architecture

### System Overview

```
┌─────────────┐
│  New PDFs   │
│  (26 books) │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ PDF-to-Markdown     │
│ Converter           │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐     ┌──────────────┐
│ Skill Extraction    │────▶│ gpt-5-chat   │
│ Engine              │     │ (Azure)      │
└──────┬──────────────┘     └──────────────┘
       │
       ▼
┌─────────────────────┐
│ Skill Taxonomy      │
│ (JSON Database)     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Filter & Prioritize │
│ (Financial Focus)   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐     ┌──────────────┐
│ Notebook Generator  │────▶│ gpt-5-mini   │
│ (3-5 demos)         │     │ (Azure)      │
└──────┬──────────────┘     └──────────────┘
       │
       ▼
┌─────────────────────┐
│ Validation Engine   │
│ (Execute & Verify)  │
└─────────────────────┘
```

### Components

#### 1. PDF Processing Layer
**Script:** `scripts/process_new_pdfs.py`

- Converts PDFs to structured markdown
- Preserves chapter/section hierarchy
- Output: `references/_markdown/{book_name}.md`

#### 2. Skill Extraction Engine
**Script:** `scripts/extract_skills_taxonomy.py`  
**Model:** Azure OpenAI `gpt-5-chat`

**Process:**
1. Load markdown files for new PDFs
2. Analyze chapter-by-chapter using LLM
3. Extract: skill name, description, category, difficulty, financial relevance
4. Generate structured JSON per book
5. Consolidate into master taxonomy

**Output Files:**
- `references/_skill_taxonomy/{book_name}_skills.json` (individual)
- `references/_skill_taxonomy/master_taxonomy.json` (consolidated)

#### 3. Skill Taxonomy Database

**JSON Schema:**
```json
{
  "book_title": "Financial Data Engineering",
  "extraction_date": "2025-11-23",
  "skills": [
    {
      "skill_id": "fin_001",
      "skill_name": "Portfolio Return Calculation",
      "category": "portfolio_analysis",
      "subcategory": "performance_metrics",
      "description": "Calculate time-weighted and money-weighted returns",
      "source_chapter": "Chapter 3: Performance Metrics",
      "difficulty": "intermediate",
      "prerequisites": ["pandas basics", "time series"],
      "financial_relevance": 10,
      "keywords": ["returns", "TWR", "MWR", "performance"],
      "example_context": "Shows calculation using pandas with daily price data"
    }
  ]
}
```

**Category Taxonomy:**
- `portfolio_analysis`: returns, attribution, optimization, rebalancing
- `risk_metrics`: VaR, CVaR, volatility, beta, Sharpe ratio, drawdown
- `time_series`: forecasting, decomposition, stationarity, ARIMA
- `statistical_methods`: hypothesis testing, regression, distributions
- `data_cleaning`: missing data, outliers, validation
- `visualization`: financial charts, dashboards, interactive plots

#### 4. Filter & Prioritize
**Script:** `scripts/filter_financial_skills.py`  
**Model (optional):** Azure OpenAI `text-embedding-3-large` for similarity detection

**Process:**
1. Filter skills where `financial_relevance >= 8`
2. Deduplicate similar skills across books
3. Rank by relevance and difficulty balance
4. Output top candidates

**Output:** `references/_skill_taxonomy/finance_focused_skills.json`

#### 5. Notebook Generation Engine
**Script:** `scripts/generate_demo_notebooks.py`  
**Model:** Azure OpenAI `gpt-5-mini`

**Selection:**
- Pick 3-5 skills covering diverse categories
- Balance difficulty (mix intermediate + 1 advanced)
- Create generation manifest

**Notebook Template Structure:**
```markdown
# [Skill Name]: [Practical Title]
*Financial Analytics Demo for [Company Name]*

## 1. Executive Summary
- What: Brief description of skill and business value
- Why: Relevance to portfolio/investment/risk management
- Key Metrics: What we'll calculate

## 2. Environment Setup
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

## 3. Synthetic Data Generation
- Generate realistic financial data
- Document assumptions (252 trading days, normal returns)
- 5-10 stocks, 2-5 years daily prices
- Realistic parameters: 8-12% annual returns, 15-25% volatility
- Risk-free rate: 4%

## 4. Analysis & Implementation
- Step-by-step code with narrative explanations
- Best practices highlighted
- Edge cases handled

## 5. Visualization
- Clear, professional charts
- Annotated insights

## 6. Key Takeaways
- Business interpretation
- When to use this technique
- Extensions/next steps
```

**Output:** `demos/interview_prep/01_portfolio_returns.ipynb` (etc.)

#### 6. Validation Engine
**Script:** `scripts/validate_notebooks.py`

**Process:**
1. Execute all cells in generated notebooks
2. Verify no errors
3. Check visualizations render
4. Report pass/fail with error details

---

## Configuration

### Azure OpenAI Setup

**Environment Variables:** `scripts/.env.local`

```bash
AZURE_API_KEY="[key]"
AZURE_ENDPOINT="https://ps-ai-project-resource.cognitiveservices.azure.com/"
AZURE_API_VERSION="2025-04-01-preview"
AZURE_CHAT_DEPLOYMENT_NAME="gpt-5-chat"      # Skill extraction
AZURE_MINI_DEPLOYMENT_NAME="gpt-5-mini"      # Notebook generation
AZURE_EMBEDDING_DEPLOYMENT="text-embedding-3-large"  # Optional: similarity
```

**Model Selection:**
- **gpt-5-chat:** Complex reasoning for skill extraction and context understanding
- **gpt-5-mini:** Cost-effective code generation for notebooks
- **text-embedding-3-large:** Optional deduplication via similarity scoring

### Configuration Class

```python
# scripts/config.py
from dataclasses import dataclass
import os
from dotenv import load_dotenv

@dataclass
class AzureConfig:
    api_key: str
    endpoint: str
    api_version: str
    chat_model: str
    mini_model: str
    embedding_model: str
    
    @classmethod
    def from_env(cls):
        load_dotenv('scripts/.env.local')
        return cls(
            api_key=os.getenv('AZURE_API_KEY'),
            endpoint=os.getenv('AZURE_ENDPOINT'),
            api_version=os.getenv('AZURE_API_VERSION'),
            chat_model=os.getenv('AZURE_CHAT_DEPLOYMENT_NAME'),
            mini_model=os.getenv('AZURE_MINI_DEPLOYMENT_NAME'),
            embedding_model=os.getenv('AZURE_EMBEDDING_DEPLOYMENT')
        )
```

---

## Workflow

### End-to-End Execution

```bash
# Step 1: Identify new PDFs added today
uv run python scripts/process_new_pdfs.py --list-new

# Step 2: Convert PDFs to markdown
uv run python scripts/process_new_pdfs.py \
  --pdfs "Financial Data Engineering.pdf,Practical Statistics for Data Scientists.pdf"

# Step 3: Extract skills using gpt-5-chat
uv run python scripts/extract_skills_taxonomy.py \
  --pdfs "Financial Data Engineering.pdf,Practical Statistics for Data Scientists.pdf" \
  --model chat \
  --output references/_skill_taxonomy/

# Step 4: Filter to financial focus
uv run python scripts/filter_financial_skills.py \
  --threshold 8 \
  --categories portfolio_analysis,risk_metrics \
  --output references/_skill_taxonomy/finance_focused_skills.json

# Step 5: Generate 3-5 demo notebooks using gpt-5-mini
uv run python scripts/generate_demo_notebooks.py \
  --skills-file references/_skill_taxonomy/finance_focused_skills.json \
  --model mini \
  --count 5 \
  --output demos/interview_prep/

# Step 6: Validate generated notebooks
uv run python scripts/validate_notebooks.py \
  --notebook-dir demos/interview_prep/
```

### Interactive Mode (Alternative)

```bash
# Step 3: Interactive skill selection
uv run python scripts/extract_skills_taxonomy.py --interactive

# Step 5: Interactive notebook generation
uv run python scripts/generate_demo_notebooks.py \
  --skills-file references/_skill_taxonomy/finance_focused_skills.json \
  --interactive
```

---

## Data Flow

```
PDFs (26 books)
    ↓ (process_new_pdfs.py)
Markdown files
    ↓ (extract_skills_taxonomy.py + gpt-5-chat)
Individual JSON skill files
    ↓ (consolidation)
master_taxonomy.json
    ↓ (filter_financial_skills.py)
finance_focused_skills.json (filtered, ranked)
    ↓ (selection: 3-5 skills)
generation_manifest.json
    ↓ (generate_demo_notebooks.py + gpt-5-mini)
Jupyter Notebooks (.ipynb)
    ↓ (validate_notebooks.py)
Validated, executable demos
```

---

## Error Handling

### PDF Processing
- **Missing PDFs:** Skip with warning, continue with available files
- **Corrupt PDFs:** Log error, mark as failed in processing report

### LLM Extraction
- **Rate limits:** Exponential backoff with retry (max 3 attempts)
- **API errors:** Log error, skip chapter, continue with next
- **Invalid JSON:** Retry with stricter prompt, fallback to manual parsing

### Notebook Generation
- **Generation failures:** Retry once, log error if persistent
- **Invalid code:** Mark notebook as "needs review", continue
- **Import errors:** Validate against allowed libraries list before generation

### Validation
- **Execution errors:** Report specific cell with error, line number
- **Missing outputs:** Flag as warning (may be intentional)
- **Timeout:** Kill execution after 5 minutes, mark as failed

---

## Quality Assurance

### Skill Extraction Quality
- Manual spot-check: Review 10% of extracted skills
- Verify financial_relevance scores are reasonable
- Check for duplicate skills across books

### Notebook Quality
- All generated code must execute without errors
- Visualizations must render properly
- Narrative must be professional and interview-ready
- Financial calculations must be accurate (spot-check formulas)

### Success Criteria
- 80%+ PDFs successfully processed
- 50+ skills extracted with financial_relevance >= 8
- 3-5 notebooks generated and validated
- All notebooks execute without errors
- Professional quality suitable for interview demonstration

---

## Cost Estimation

### Azure OpenAI Token Usage (Estimates)

**Skill Extraction (gpt-5-chat):**
- Input: ~500K tokens (26 books, assuming 20K tokens per book)
- Output: ~100K tokens (skill descriptions)
- Total: ~600K tokens

**Notebook Generation (gpt-5-mini):**
- Input: ~10K tokens per notebook (5 notebooks)
- Output: ~15K tokens per notebook (code + narrative)
- Total: ~125K tokens

**Total Estimated:** ~725K tokens across both models

*(Actual costs depend on Azure OpenAI pricing tier)*

---

## Future Enhancements

1. **Incremental Processing:** Only process newly added PDFs, skip existing
2. **Skill Versioning:** Track changes to skills over time as books are updated
3. **Interactive Dashboard:** Web UI to browse skill taxonomy and select demos
4. **Skill Relationships:** Build dependency graph (prerequisites, related skills)
5. **Multi-Language Support:** Generate notebooks in R or Julia for comparison
6. **Automated Testing:** Unit tests for generated financial calculations
7. **Portfolio Website:** Deploy demos to GitHub Pages for portfolio showcase

---

## Dependencies

### Python Packages
```toml
[project.dependencies]
pandas = ">=2.0.0"
numpy = ">=1.24.0"
matplotlib = ">=3.7.0"
seaborn = ">=0.12.0"
plotly = ">=5.14.0"
jupyter = ">=1.0.0"
openai = ">=1.0.0"  # Azure OpenAI SDK
python-dotenv = ">=1.0.0"
pdfplumber = ">=0.9.0"  # PDF processing
```

### External Services
- Azure OpenAI API (gpt-5-chat, gpt-5-mini, text-embedding-3-large)

---

## Timeline

**Day 1:**
- Implement PDF processing and skill extraction scripts
- Extract skills from all 26 PDFs
- Create filtered finance-focused taxonomy

**Day 2:**
- Implement notebook generation script
- Generate 3-5 demo notebooks
- Validate and refine outputs
- Final review and polish

---

## Success Metrics

- ✅ Exhaustive skill taxonomy created (JSON database)
- ✅ 50+ finance-relevant skills identified and ranked
- ✅ 3-5 professional Jupyter notebooks generated
- ✅ All notebooks execute without errors
- ✅ Demonstrations showcase portfolio, investment, and risk analytics
- ✅ Interview-ready quality (professional narrative + working code)

---

## Appendix: Example Skills

### Portfolio Analysis
- Time-weighted vs. money-weighted returns
- Portfolio attribution analysis
- Mean-variance optimization
- Efficient frontier calculation
- Rebalancing strategies

### Risk Metrics
- Value at Risk (VaR) - Historical, Parametric, Monte Carlo
- Conditional VaR (CVaR / Expected Shortfall)
- Sharpe ratio, Sortino ratio, Calmar ratio
- Beta and systematic risk
- Maximum drawdown analysis

### Time Series
- ARIMA forecasting for returns
- Volatility clustering (GARCH models)
- Stationarity testing
- Rolling window analysis

### Visualization
- Candlestick charts
- Portfolio performance dashboards
- Risk heatmaps
- Correlation matrices
- Interactive Plotly financial charts
