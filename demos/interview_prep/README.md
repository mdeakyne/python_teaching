# Financial Analytics Demo Notebooks

Professional Jupyter notebooks demonstrating portfolio, investment, and risk analytics skills.

## Purpose

These notebooks were created for interview preparation, showcasing:
- Portfolio analysis techniques
- Risk metric calculations
- Time series forecasting
- Data visualization best practices
- Production-quality Python code

## Generated Notebooks

Each notebook is self-contained with:
- Executive summary of the technique
- Synthetic financial data generation
- Step-by-step implementation
- Professional visualizations
- Business insights and takeaways

## Running the Notebooks

### Prerequisites

```bash
# Ensure you're in the project root
cd /path/to/python_teaching

# Install dependencies
uv sync
```

### Launch Jupyter Lab

```bash
cd demos/interview_prep
uv run jupyter lab
```

### Execute Notebooks

Each notebook can be run top-to-bottom:
1. Select a notebook from the file browser
2. Click "Run" → "Run All Cells"
3. Wait for execution to complete
4. Review outputs and visualizations

## Notebooks Overview

| # | Skill | Category | Difficulty |
|---|-------|----------|------------|
| (Auto-generated - see notebook files) |

## Data

All notebooks use synthetic financial data generated within the notebook:
- **Stocks:** 5-10 realistic symbols (AAPL, MSFT, GOOGL, etc.)
- **Time Period:** 2-5 years of daily prices
- **Parameters:** 8-12% annual returns, 15-25% volatility
- **Risk-Free Rate:** 4%
- **Trading Days:** 252 per year

## Customization

To customize for specific interviews:

1. **Company Name:** Update executive summary sections
2. **Stock Universe:** Modify data generation to use sector-specific stocks
3. **Time Period:** Adjust date ranges in data generation
4. **Visualizations:** Customize colors/themes to match company branding

## Regeneration

To regenerate notebooks with different skills:

```bash
cd scripts

# See available skills
python filter_financial_skills.py

# Generate new notebooks (interactive selection)
python generate_demo_notebooks.py --interactive --count 3
```

## Validation

To validate all notebooks execute without errors:

```bash
cd scripts
python validate_notebooks.py --notebook-dir ../demos/interview_prep --execute
```

## Interview Tips

1. **Know the Business Context:** Be ready to explain why each metric matters
2. **Discuss Trade-offs:** Every technique has limitations - know them
3. **Production Considerations:** How would you scale this? Monitor it? Handle errors?
4. **Alternatives:** What other approaches could solve this problem?
5. **Next Steps:** How would you extend this analysis?

## Questions?

Review the source code in `scripts/` to understand how these were generated.
