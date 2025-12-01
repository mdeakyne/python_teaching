# Distributed Customer Analytics with Dask

## Context

### Business Scenario

StoryBoard Analytics has accumulated 5 million customer interactions (browsing, purchases, reviews) over 2 years. The current pandas-based analytics pipeline takes 6+ hours to run, blocking the daily reporting cycle. As the business grows, this processing time will only increase.

### Your Role: Data Platform Engineer

**Challenge:** Single-node pandas processing can't scale with growing data volumes

**Goal:** Implement distributed processing with Dask to handle multi-GB datasets efficiently, reducing processing time to under 1 hour

## Learning Objectives

**Skills You'll Practice:**

- Growth Decomposition Analysis (advanced)
- 2×2 Experimental Design (intermediate)
- Building Data-Driven Business Cases (intermediate)
- Lift Analysis (intermediate)
- Data Storytelling and Narrative Development (beginner)

**Key Concepts:**

- additive decomposition
- multiplicative decomposition
- factorial design
- interaction analysis
- ROI estimation
- cost-benefit analysis
- lift calculation
- baseline comparison
- clarity
- engagement

## Requirements

### Functional Requirements

**FR1: Distributed Data Loading**
- Load multi-GB datasets (sales, customers, reviews) using Dask
- Automatic partitioning based on data size
- Memory-efficient lazy loading

**FR2: Customer Segmentation Analysis**
- Segment customers by purchase behavior, genre preferences
- Calculate RFM (Recency, Frequency, Monetary) scores
- Identify high-value customer cohorts

**FR3: Product Affinity Analysis**
- Calculate book co-purchase patterns
- Generate recommendation candidates
- Handle sparse interaction matrices efficiently

**FR4: Performance Optimization**
- Process 5M interactions in <1 hour
- Use <16GB memory (laptop-friendly)
- Graceful degradation on smaller machines

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
distributed-customer-analytics-with-dask/
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

**customers.csv** (200K customers, ~50MB)
- Customer profiles and segments
- Columns: `customer_id`, `signup_date`, `city`, `state`

**transactions.csv** (5M transactions, ~500MB)
- Purchase history over 2 years
- Columns: `transaction_id`, `timestamp`, `customer_id`, `book_isbn`, `quantity`, `price`

**reviews.csv** (500K reviews, ~100MB)
- Customer book reviews
- Columns: `review_id`, `customer_id`, `book_isbn`, `rating`, `review_text`, `timestamp`

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

1. **Multi-Node Cluster** - Deploy to actual Dask cluster
2. **GPU Acceleration** - Use Dask-cuDF for GPU processing
3. **Advanced ML** - Add collaborative filtering recommender
4. **Production Deployment** - Containerize with Docker

## Resources

### Reading Materials


### Tools & Libraries

- Python 3.11+
- Dask (distributed DataFrame)
- pandas compatibility layer
- pytest for testing

---

**Estimated Time:** 46 hours
**Difficulty:** Advanced
**Skills Practiced:** 5
