# Real-Time Book Sales Analytics Pipeline

## Context

### Business Scenario

StoryBoard Analytics operates 50+ bookstores across the US, each processing hundreds of transactions daily. Currently, sales data is batch-processed overnight, creating a 24-hour lag in insights. This delay means:
- Store managers can't respond to real-time inventory issues
- Marketing can't capitalize on trending books
- Fraud detection is delayed by a day
- Customer service lacks up-to-date purchase information

### Your Role: Data Engineer

**Challenge:** The 24-hour data lag prevents timely business decisions

**Goal:** Build a real-time streaming pipeline to process sales events as they happen, enabling instant insights and alerts

## Learning Objectives

**Skills You'll Practice:**

- Stateful Stream Transformations (advanced)
- Streaming Database Architecture (advanced)
- Consistency Models in Stream Processing (advanced)
- Designing Actionable, Timely, and Relevant Metrics (intermediate)
- Metrics Decomposition (intermediate)

**Key Concepts:**

- state management
- windowing
- row-based vs column-based
- edge streaming
- ACID
- eventual consistency
- measurability
- actionability
- funnel analysis
- stock-flow relationships

## Requirements

### Functional Requirements

**FR1: Event Ingestion**
- Ingest sales events from multiple stores in real-time
- Input: JSON events with `timestamp`, `store_id`, `book_isbn`, `quantity`, `price`
- Handle 500-2000 events/second during peak hours
- Validate schema and reject malformed events

**FR2: Real-Time Aggregation**
- Calculate rolling metrics: revenue by store, sales by genre, top books
- Update aggregations within 100ms of event arrival
- Support time windows: last 1h, last 24h, last 7 days

**FR3: Data Quality Monitoring**
- Detect anomalies: sudden sales spikes, missing store data
- Alert on data quality issues (>5% invalid events)
- Log all errors with context for debugging

**FR4: Query API**
- REST API to query current metrics
- Endpoints: `/metrics/revenue`, `/metrics/top-books`, `/metrics/store/{id}`
- Response time: <50ms for standard queries

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
real-time-book-sales-analytics-pipeline/
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

**sales_events.jsonl** (100K events, ~15MB)
- Real-time sales events from 50 stores
- Columns: `timestamp`, `store_id`, `book_isbn`, `quantity`, `price`, `customer_id`
- Time span: 30 days
- Quality issues: ~2% missing `store_id`, ~0.5% invalid ISBN

**stores.csv** (50 stores)
- Store metadata for enrichment
- Columns: `store_id`, `name`, `city`, `state`, `timezone`

**books.csv** (10K books)
- Book catalog with genres
- Columns: `isbn`, `title`, `author`, `genre`, `price`

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

1. **Exactly-Once Semantics** - Implement idempotent processing
2. **Backpressure Handling** - Gracefully handle event surges
3. **Cloud Deployment** - Deploy to AWS/GCP with auto-scaling
4. **Monitoring Dashboard** - Grafana/Prometheus integration

## Resources

### Reading Materials


### Tools & Libraries

- Python 3.11+
- Kafka or simulated stream (JSON files)
- pandas for aggregations
- FastAPI for REST API

---

**Estimated Time:** 60 hours
**Difficulty:** Advanced
**Skills Practiced:** 5
