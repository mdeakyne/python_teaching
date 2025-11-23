# Financial Analytics Demo Notebooks

Professional Jupyter notebooks demonstrating portfolio, investment, and risk analytics skills.

## Purpose

These notebooks were created for interview preparation, showcasing:
- Portfolio analysis techniques
- Risk metric calculations
- Time series forecasting
- Data visualization best practices
- Production-quality Python code

## Consulting-Style Analysis Reports

Professional financial consulting reports demonstrating strategic decision support:

### Family Office Reports

**1. Portfolio Rebalancing Analysis** (`fo-rebalancing.ipynb`)
- **Client:** Harrison Family Office
- **Question:** Should we rebalance after tech sector gains?
- **Skills:** Portfolio attribution, sector concentration, risk metrics, rebalancing analysis
- **Duration:** ~25 minutes

**2. Exit Strategy Analysis** (`fo-exit.ipynb`)
- **Client:** Harrison Family Office
- **Question:** Should we exit an underperforming legacy holding?
- **Skills:** Position performance, opportunity cost, risk-adjusted returns, tax considerations
- **Duration:** ~20 minutes

### Wealth Management Reports

**3. Client Onboarding Portfolio Recommendation** (`wm-onboarding.ipynb`)
- **Client:** Apex Wealth Management
- **Question:** What portfolio should we recommend for a new client?
- **Skills:** Asset allocation, Modern Portfolio Theory, efficient frontier, diversification
- **Duration:** ~30 minutes

**4. Portfolio Stress Testing** (`wm-stress-test.ipynb`)
- **Client:** Apex Wealth Management
- **Question:** How resilient is the portfolio to market downturns?
- **Skills:** VaR, CVaR, maximum drawdown, stress scenarios, recovery analysis
- **Duration:** ~25 minutes

## Report Structure

Each consulting notebook follows professional report format:

1. **Executive Summary** - Key findings and recommendations upfront
2. **Situation Overview** - Business context and current state
3. **Data & Methodology** - Analytical approach and assumptions
4. **Analysis** - Multiple sections with insights
5. **Visualizations** - Professional charts with business interpretation
6. **Risk Considerations** - Limitations and assumptions
7. **Recommendations** - Specific, actionable guidance
8. **Next Steps** - Implementation roadmap

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

## Generated Notebooks

Each notebook is self-contained with:
- Executive summary and structured storyline
- Synthetic financial data generation
- Step-by-step implementation
- Professional visualizations
- Business insights and next steps

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

To regenerate consulting notebooks:

```bash
cd scripts

# List available consulting scenarios
uv run python generate_consulting_notebooks.py --list

# Generate all consulting notebooks
uv run python generate_consulting_notebooks.py --scenarios all --model mini

# Generate a subset
uv run python generate_consulting_notebooks.py --scenarios fo_rebalancing,wm_stress_test

# Offline / deterministic template mode
uv run python generate_consulting_notebooks.py --scenarios all --no-llm

> Tip: The CLI automatically falls back to the deterministic template if the Azure OpenAI call fails.
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
