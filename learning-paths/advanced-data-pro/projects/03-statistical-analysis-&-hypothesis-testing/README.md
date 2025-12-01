# Statistical Analysis & Hypothesis Testing

## Context

### Business Scenario

StoryBoard Analytics runs frequent A/B tests and promotional campaigns but lacks rigorous statistical analysis. Marketing makes decisions based on directional trends rather than statistical significance, leading to suboptimal outcomes.

### Your Role: Data Analyst

**Challenge:** Business decisions lack statistical rigor and confidence intervals

**Goal:** Build a statistical analysis framework for hypothesis testing, experiment design, and data-driven decision making

## Learning Objectives

**Skills You'll Practice:**

- Implement Stateful Applications with Ray Actors (intermediate)
- Build Workflow Management in Ray (intermediate)
- Use Ray for Batch and Stream Processing (intermediate)
- Apply Advanced Data Processing with Ray (advanced)
- Build Microservices with Ray Serve (intermediate)

**Key Concepts:**

- actor model
- state persistence
- workflow orchestration
- task scheduling
- batch jobs
- streaming pipelines
- fault tolerance
- serialization
- microservice architecture
- deployment composition

## Requirements

### Functional Requirements

**FR1: Hypothesis Testing Framework**
- Support t-tests, chi-square tests, ANOVA
- Calculate p-values, confidence intervals, effect sizes
- Report statistical significance with context

**FR2: A/B Test Analysis**
- Compare conversion rates between test groups
- Power analysis: determine required sample sizes
- Multiple testing correction (Bonferroni, FDR)

**FR3: Lift & Impact Analysis**
- Calculate lift from promotions/campaigns
- Decompose metrics (P×Q analysis)
- Estimate ROI with uncertainty bounds

**FR4: Visualization & Reporting**
- Generate statistical plots (distributions, confidence intervals)
- Create executive summaries of findings
- Export results to markdown/HTML reports

### Non-Functional Requirements

**Performance:**
- See functional requirements for specific targets

**Code Quality:**
- Follow PEP 8 (enforced with `black`, `flake8`)
- Type hints for all functions
- Docstrings for public APIs
- No commented-out code in final submission

**Testing:**
- Unit tests for core logic (>80% coverage)
- Integration test for end-to-end flow
- Performance benchmarks

## Acceptance Criteria

### Functional Completeness
- [ ] All functional requirements implemented
- [ ] Edge cases handled gracefully
- [ ] Error handling with clear messages

### Performance
- [ ] Meets throughput/latency targets
- [ ] Handles specified data volumes
- [ ] Resource usage within bounds

### Code Quality
- [ ] Passes `black` and `flake8`
- [ ] Type hints present
- [ ] Well-organized file structure
- [ ] Clear variable/function names

### Testing & Documentation
- [ ] Unit tests pass (>80% coverage)
- [ ] Integration test passes
- [ ] README with setup/usage
- [ ] Architecture documented

## Deliverables

### Code Repository Structure

```
statistical-analysis-&-hypothesis-testing/
├── README.md              # Project overview, setup, usage
├── pyproject.toml         # Dependencies (uv-compatible)
├── src/
│   ├── __init__.py
│   ├── [main modules]
├── tests/
│   ├── test_[module].py
├── data/
│   └── [sample data]
└── docs/
    └── architecture.md    # Design decisions
```

### Documentation
- **README.md:** Overview, setup instructions, usage examples
- **architecture.md:** System design, data flow, key decisions

## Data

### Sample Datasets (Provided)

Located in `data-samples/`:

**ab_test_results.csv** (10K samples)
- A/B test data from email campaign
- Columns: `customer_id`, `test_group`, `opened`, `clicked`, `purchased`

**promotion_lift.csv** (50K transactions)
- Before/after promotion data
- Columns: `timestamp`, `promotion_active`, `book_isbn`, `quantity`, `revenue`

### Expected Data Volumes

- **Development:** Small samples (1K-10K records)
- **Testing:** Medium samples (100K-1M records)
- **Stress Testing:** Large samples (1M+ records)

## Self-Assessment

Use `evaluation.md` in this directory for detailed rubric.

**Quick Check:**
- All features work? (40 pts)
- Code quality good? (30 pts)
- Performance targets met? (20 pts)
- Tests passing? (10 pts)

**90+ points = Excellent, ready for portfolio!**

## Extension Ideas

Optional enhancements for deeper learning:

1. **Bayesian Analysis** - Add Bayesian A/B testing
2. **Sequential Testing** - Implement early stopping rules
3. **Causal Inference** - Add propensity score matching
4. **Interactive Dashboard** - Build Dash app for analysis

## Resources

### Reading Materials


### Tools & Libraries

- Python 3.11+
- scipy.stats for hypothesis tests
- statsmodels for advanced stats
- matplotlib/seaborn for visualization

---

**Estimated Time:** 50 hours
**Difficulty:** Intermediate
**Skills Practiced:** 5
