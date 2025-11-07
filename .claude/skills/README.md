# Claude Skills for Python Data Analysis

This directory contains Claude-based skills tailored to the Python teaching content in this repository. These skills help with pandas, data analysis, visualization, and Dash dashboard development.

## Available Skills

### 1. **pandas-helper**
Expert assistant for pandas data manipulation tasks.

**Use when you need help with:**
- Creating and manipulating DataFrames
- Data selection, filtering, and querying
- GroupBy operations and aggregations
- Merging and joining datasets
- Time series operations
- Data transformation and reshaping

**Example usage:**
```
Use the pandas-helper skill to help me merge sales and books data and find the top-selling books by genre
```

---

### 2. **data-cleaning**
Expert assistant for data cleaning and quality tasks.

**Use when you need help with:**
- Handling missing values (NaN, null)
- Detecting and removing duplicates
- Fixing data types and conversions
- Cleaning string data
- Detecting and handling outliers
- Data validation and consistency checks

**Example usage:**
```
Use the data-cleaning skill to help me handle missing dates and clean up the price column that has dollar signs
```

---

### 3. **visualization**
Expert assistant for creating visualizations with matplotlib, seaborn, and plotly.

**Use when you need help with:**
- Choosing the right chart type for your data
- Creating bar charts, line plots, scatter plots
- Statistical visualizations (box plots, histograms, heatmaps)
- Interactive Plotly charts
- Professional styling and theming
- Multi-panel layouts and subplots

**Example usage:**
```
Use the visualization skill to create an interactive scatter plot showing the relationship between book price and sales
```

---

### 4. **dash-builder**
Expert assistant for building interactive Dash dashboards.

**Use when you need help with:**
- Setting up Dash apps
- Creating layouts with components
- Building callbacks for interactivity
- Adding dropdowns, sliders, and filters
- Multi-page apps and navigation
- Styling and professional layouts
- Deployment preparation

**Example usage:**
```
Use the dash-builder skill to help me create a dashboard with a date range filter that updates both a chart and summary metrics
```

---

### 5. **dataframe-explorer**
Expert assistant for exploring and understanding DataFrames.

**Use when you need help with:**
- Initial data inspection and profiling
- Understanding data types and distributions
- Finding missing values and duplicates
- Generating summary statistics
- Detecting outliers
- Quick exploratory visualizations

**Example usage:**
```
Use the dataframe-explorer skill to help me understand what's in this new sales dataset I just loaded
```

---

### 6. **data-analysis**
Expert assistant for exploratory data analysis and generating insights.

**Use when you need help with:**
- Answering analytical questions about data
- Top N analyses and rankings
- Trend analysis over time
- Segmentation and cohort analysis
- Correlation and relationship discovery
- Comparative analysis between groups
- Generating actionable insights

**Example usage:**
```
Use the data-analysis skill to help me understand which authors are driving the most revenue and if there's a concentration problem
```

---

## How to Use Skills

Skills can be invoked in Claude by using the skill name. When you activate a skill, Claude will adopt the specific expertise and patterns defined in that skill.

### Tips for Effective Use

1. **Choose the right skill** - Match your task to the skill's specialty
2. **Be specific** - Provide context about your data and what you want to achieve
3. **Chain skills** - Use multiple skills in sequence for complex workflows:
   - Start with `dataframe-explorer` to understand new data
   - Use `data-cleaning` to fix quality issues
   - Apply `pandas-helper` for complex manipulations
   - Use `data-analysis` to answer questions
   - Create visuals with `visualization`
   - Build dashboards with `dash-builder`

### Example Workflows

**Workflow 1: New Dataset Analysis**
1. `dataframe-explorer` - Understand the data structure
2. `data-cleaning` - Fix any quality issues
3. `data-analysis` - Answer analytical questions
4. `visualization` - Create compelling charts

**Workflow 2: Building a Dashboard**
1. `pandas-helper` - Prepare and aggregate data
2. `visualization` - Create individual charts
3. `dash-builder` - Assemble into interactive dashboard

**Workflow 3: Report Generation**
1. `data-analysis` - Generate insights
2. `visualization` - Create publication-ready charts
3. `pandas-helper` - Export summary tables

---

## Skill Development

These skills are based on the 21-Day Pandas & Dash Visualization Bootcamp content in this repository:

- **Week 1** (Days 1-7): Pandas foundations → `pandas-helper`, `data-cleaning`, `dataframe-explorer`
- **Week 2** (Days 8-14): Visualization → `visualization`
- **Week 3** (Days 15-21): Dash dashboards → `dash-builder`, `data-analysis`

---

## Contributing

To add or modify skills:

1. Create or edit a `.md` file in `.claude/skills/`
2. Include a YAML front matter with `description` and `tags`
3. Provide clear guidelines, code patterns, and examples
4. Update this README with the new skill documentation

---

## Related Resources

- [Main README](../../README.md) - Repository overview
- [Bootcamp Documentation](../../docs/index.md) - Full course materials
- [Day-by-day lessons](../../docs/) - Detailed tutorials for each topic

---

**Happy data analyzing!** 🐼📊✨
