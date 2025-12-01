# Advanced Data Professional Learning Path

**Welcome to the StoryBoard Analytics Learning Journey!** 🐗

## What Is This?

This is a **project-based learning curriculum** designed for intermediate Python developers who want to advance in:
- **Data Engineering** - Streaming pipelines, distributed systems, data mesh
- **Data Science** - Statistical analysis, distributed computing with Dask/Ray  
- **Visualization** - Data storytelling and dashboards
- **Clean Code** - Production-ready, performant systems

## Who Is This For?

**You're a good fit if you:**
- Already know Python well (functions, classes, basic pandas)
- Want hands-on practice with real-world data systems
- Prefer **spec-based projects** (requirements, not tutorials)
- Can dedicate **3 hours/week over 6 months**
- Want portfolio-worthy projects

**Not a beginner?** Perfect. This path assumes you know the basics and focuses on advanced, production-oriented skills.

## The StoryBoard Analytics Universe 🐗

All projects use data from **StoryBoard Analytics**, a fictional multi-channel bookstore:
- **50+ store locations** across the US
- **500K+ active customers**  
- **2M+ books sold annually**
- **Real-world challenges:** streaming data, distributed processing, statistical analysis, data governance

**Why a bookstore?** Books provide rich, realistic data (genres, authors, reviews, sales patterns) that's relatable and interesting to analyze.

**Meet Wally the Warthog:** Your data-driven guide through this learning journey. Tough, persistent, and sharp at cutting through complexity!

## What You'll Build

### Project 1: Real-Time Book Sales Analytics Pipeline
**Duration:** 14-15 weeks (41 hours)  
**Difficulty:** Intermediate

Build a streaming pipeline that processes book sales events in real-time, enabling instant insights and alerts.

**Skills:** Stream processing, materialized views, CDC, real-time queries

**Deliverable:** Production-ready streaming system handling 1000+ events/second

---

### Project 2: Distributed Customer Analytics with Dask
**Duration:** 15-16 weeks (44 hours)  
**Difficulty:** Intermediate

Analyze millions of customer interactions using distributed computing, reducing processing time from 6+ hours to under 1 hour.

**Skills:** Distributed processing, metrics design, experimental design, business analysis

**Deliverable:** Scalable analytics pipeline processing multi-GB datasets

---

### Project 3: Statistical Analysis & Hypothesis Testing
**Duration:** 15-16 weeks (44 hours)  
**Difficulty:** Intermediate

Build a rigorous statistical analysis framework for A/B testing, experiment design, and data-driven decision making.

**Skills:** Hypothesis testing, experimental design, lift analysis, data storytelling

**Deliverable:** Statistical analysis toolkit with visualization and reporting

---

### Project 4: Production Data Mesh Implementation
**Duration:** 17-18 weeks (51 hours)  
**Difficulty:** Advanced

Design and implement data mesh architecture with domain-oriented ownership, data as a product, and federated governance.

**Skills:** Data mesh architecture, data governance, data products, organizational design

**Deliverable:** Functional data mesh with multiple domain data products

---

## How It Works

### 1. Spec-Based Learning

Each project provides:
- **Business scenario** - Realistic context from StoryBoard Analytics
- **Requirements** - Functional and non-functional specs
- **Acceptance criteria** - Testable conditions for "done"
- **Sample data** - Realistic datasets with quality issues
- **Self-assessment rubric** - 100-point scoring system

**You design, plan, and implement.** Use AI tools if you want, but the planning phase is critical.

### 2. Learning Flow

For each project:

1. **Read** assigned PDF chapters (listed in curriculum)
2. **Review** project spec and requirements
3. **Plan** your architecture and approach
4. **Implement** following clean code principles
5. **Test** against acceptance criteria
6. **Self-assess** using evaluation rubric
7. **Iterate** based on gaps

### 3. Progressive Difficulty

- **Week 1-15:** Intermediate projects (streaming, distributed processing, statistics)
- **Week 16-24:** Advanced project (data mesh architecture)
- Each project builds on skills from previous ones
- Cumulative learning: later projects assume earlier skills mastered

## Repository Structure

```
learning-paths/advanced-data-pro/
├── 00-overview.md              # This file
├── 01-skill-graph.md           # Visual map of all 62 skills
├── 02-curriculum.md            # Full curriculum with all 4 projects
└── projects/
    ├── 01-real-time-book-sales-analytics-pipeline/
    │   ├── README.md           # Project spec
    │   ├── evaluation.md       # Self-assessment rubric
    │   └── data-samples/       # Sample datasets
    ├── 02-distributed-customer-analytics-with-dask/
    ├── 03-statistical-analysis-&-hypothesis-testing/
    └── 04-production-data-mesh-implementation/
```

## Getting Started

### Prerequisites

**Software:**
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Git for version control
- Your favorite IDE/editor

**Knowledge:**
- Python fundamentals (you're comfortable with the language)
- Basic pandas (DataFrames, selection, groupby)
- Basic SQL (SELECT, JOIN, WHERE)

### Step 1: Review the Curriculum

Read [`02-curriculum.md`](02-curriculum.md) to understand the full learning path.

**Key questions to answer:**
- Does the time commitment fit your schedule (3h/week)?
- Are the projects aligned with your learning goals?
- Do you have the prerequisite knowledge?

### Step 2: Explore the Skill Graph

Review [`01-skill-graph.md`](01-skill-graph.md) to see all 62 skills and their relationships.

**This shows you:**
- Which skills build on others (prerequisites)
- Critical skills that unlock many others
- Skill categories and difficulty levels

### Step 3: Set Up Your Environment

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a workspace directory
mkdir storyboard-analytics
cd storyboard-analytics

# Create first project directory
mkdir project-01-streaming-pipeline
cd project-01-streaming-pipeline

# Initialize Python project
uv init
```

### Step 4: Start Project 1

1. Read the project spec: `projects/01-real-time-book-sales-analytics-pipeline/README.md`
2. Review assigned chapters from source PDFs (see curriculum)
3. Plan your architecture (spend time here!)
4. Start implementing

## Time Commitment

**Total:** ~181 hours over 60 weeks (at 3h/week)

**Breakdown:**
- **Reading:** ~30% (PDF chapters, documentation)
- **Planning:** ~5% (architecture, design decisions)
- **Implementation:** ~45% (coding, testing)
- **Buffer:** ~20% (learning curve, debugging, iteration)

**Flexible pacing:** Take more or less time per project based on your schedule. The ~3h/week is a guideline, not a requirement.

## Success Criteria

**You'll know you're succeeding when:**
- ✅ Projects meet all acceptance criteria
- ✅ Code is clean and well-documented
- ✅ You can explain your design decisions
- ✅ Performance benchmarks are met
- ✅ You're comfortable with the skills

**Portfolio-ready:** Aim for 90+ points on self-assessment for each project. These become showcases for job interviews or freelance work.

## Learning Resources

### Source Materials

PDFs in `/references/`:
- Scaling Python with Dask
- Scaling Python with Ray
- Practical Statistics for Data Scientists
- Data Science from Scratch 2nd Edition
- Data Science The Hard Parts
- Streaming Databases
- Financial Data Engineering
- Implementing Data Mesh

### Tools & Libraries

- **Python:** 3.11+ (with type hints)
- **Data:** pandas, Dask, Ray
- **Statistics:** scipy, statsmodels
- **Visualization:** matplotlib, seaborn, plotly
- **Testing:** pytest
- **Code Quality:** black, flake8, mypy

## Meta-Skills: How This Was Built

Curious about the process that generated this curriculum?

See [`/meta/README.md`](/meta/README.md) for:
- Process skills (PDF → markdown → skill extraction → graph → curriculum)
- Reusable meta-skills for building learning paths
- Scripts and templates

**Use these meta-skills to create your own learning paths from technical PDFs!**

## Tips for Success

### 1. Read First, Code Second

Resist the urge to jump straight to coding. Read the assigned chapters, understand the concepts, then implement.

### 2. Plan Your Architecture

Spend 2-3 hours planning before writing code. Sketch data flows, identify components, consider edge cases.

### 3. Use AI Wisely

AI tools (like Claude, ChatGPT) can help with implementation, but:
- **Do your own planning** (don't ask AI to design for you)
- **Understand every line** of AI-generated code
- **Test thoroughly** (AI makes mistakes)

### 4. Test As You Go

Don't wait until the end to write tests. Test each component as you build it.

### 5. Document Your Decisions

Keep an `architecture.md` file. When you make a design choice, write down:
- What you decided
- Why you chose that approach
- Alternatives you considered

This is valuable for interviews: "Tell me about a time you made a technical decision..."

### 6. Iterate Based on Feedback

Use the self-assessment rubric honestly. If you score below 75, refactor before moving to the next project.

## FAQ

**Q: Can I do the projects in a different order?**  
A: Not recommended. They build on each other, with skills from earlier projects assumed in later ones.

**Q: What if I get stuck?**  
A: Review the skill graph to identify prerequisite skills you may need to strengthen. Re-read source material. Use AI for specific questions, not wholesale solutions.

**Q: Can I use different tools/libraries?**  
A: Yes, but specs are written for the listed tools. Substituting (e.g., Spark instead of Dask) may require adapting requirements.

**Q: How do I know if my solution is good?**  
A: Use the evaluation rubric. 90+ points = excellent. Also: does it meet all functional requirements? Would you be proud to show this in an interview?

**Q: Can I collaborate with others?**  
A: Absolutely! Discussing approaches and reviewing each other's code is valuable. Just make sure you understand every part of your own implementation.

**Q: What if I don't have access to the PDF books?**  
A: The curriculum provides enough context to complete projects, but the books offer deeper understanding. Check your library, or focus on projects that align with books you have.

## Next Steps

1. **Read the curriculum:** [`02-curriculum.md`](02-curriculum.md)
2. **Explore the skill graph:** [`01-skill-graph.md`](01-skill-graph.md)
3. **Start Project 1:** `projects/01-real-time-book-sales-analytics-pipeline/README.md`

---

**Ready to start your journey with Wally the Warthog?** 🐗

Let's build some data systems!
