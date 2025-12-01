# Financial Services Data Governance & AI Interview Study Guide

**Interview Date:** Tuesday  
**Focus Areas:** Managed Services, Data Governance, Large-Scale Financial Data, AI/ML Integration  
**Generated:** 2025-11-23

---

## 🎯 Executive Summary

This study guide is tailored for a **managed services role in financial services** with emphasis on:
- **Data Governance** in regulated financial environments
- **Large-scale data architecture** and management
- **Protected financial data** handling and compliance
- **AI/ML integration** with governance frameworks

---

## 📊 Priority 1: Data Governance & Compliance (CRITICAL)

### Core Concepts

#### 1. Financial Data Governance Frameworks
**Financial Relevance: 10/10**

**Key Skills:**
- Establish governance frameworks ensuring data quality, compliance, and stewardship
- Implement regulatory compliance (SOX, GDPR, FINRA, etc.)
- Define metadata standards and data stewardship roles
- Manage data lineage and auditability

**Interview Talking Points:**
```
✓ Data Quality Dimensions: Accuracy, Completeness, Consistency, Timeliness
✓ Regulatory Requirements: SOX (Sarbanes-Oxley), GDPR, MiFID II, BCBS 239
✓ Stewardship Model: Data owners, custodians, consumers
✓ Metadata Management: Business, technical, operational metadata
```

**Example Scenario:**
> "How would you implement data governance for a new AI model that uses customer transaction data?"

**Answer Framework:**
1. **Classification**: Identify PII/sensitive financial data
2. **Access Control**: Role-based access, least privilege
3. **Lineage Tracking**: Document data sources → transformations → model
4. **Audit Trail**: Log all access and transformations
5. **Compliance Checks**: GDPR consent, SOX controls, model explainability
6. **Quality Metrics**: Define SLAs for accuracy, completeness

---

#### 2. Data Lineage Analysis
**Financial Relevance: 7/10**

**Key Skills:**
- Trace data origins, transformations, and movements through systems
- Ensure transparency and governance
- Enable auditability for regulatory compliance

**Technical Implementation:**
```python
# Conceptual Data Lineage Tracking
lineage_record = {
    "data_asset_id": "customer_transactions_v2",
    "source_systems": [
        {"system": "core_banking", "table": "transactions", "timestamp": "2025-11-20T09:00:00Z"},
        {"system": "fraud_detection", "table": "flagged_txns", "timestamp": "2025-11-20T09:15:00Z"}
    ],
    "transformations": [
        {"step": "deduplication", "rule": "composite_key(account_id, txn_date, amount)"},
        {"step": "pii_masking", "fields": ["ssn", "account_number"], "method": "tokenization"},
        {"step": "aggregation", "grain": "daily", "metrics": ["sum_amount", "count_txns"]}
    ],
    "consumers": [
        {"service": "risk_analytics_model", "version": "v3.2", "purpose": "credit_scoring"},
        {"service": "regulatory_reporting", "regulation": "BCBS_239"}
    ],
    "compliance_tags": ["pii_protected", "sox_controlled", "gdpr_compliant"]
}
```

**Interview Questions to Prepare:**
- How do you handle data lineage when data flows through 10+ systems?
- How would you implement automated lineage tracking for streaming data?
- What metadata is essential for regulatory audits?

---

#### 3. Data Contracts and Quality Assurance
**Financial Relevance: 8/10**

**Key Skills:**
- Define and manage data contracts for trust and versioning
- Ensure semantic clarity and quality of service (QoS)
- Implement contract-based governance in Data Mesh architectures

**Data Contract Example:**
```yaml
# Financial Transaction Data Contract v2.1
contract_id: txn_data_product_v2.1
owner: payments_domain_team
classification: HIGHLY_CONFIDENTIAL

schema:
  - name: transaction_id
    type: STRING
    required: true
    pii: false
    unique: true
    
  - name: account_number
    type: STRING
    required: true
    pii: true
    encryption: AES-256
    masking_rule: tokenize
    
  - name: amount
    type: DECIMAL(18,2)
    required: true
    validation: amount > 0
    
  - name: transaction_date
    type: TIMESTAMP
    required: true
    timezone: UTC
    
quality_sla:
  completeness: 99.9%
  accuracy: 99.99%
  timeliness: "< 5 minutes from source"
  freshness: "< 15 minutes"
  
governance:
  retention_period: 7_years  # SOX requirement
  backup_frequency: daily
  audit_logging: enabled
  access_control: role_based
  
versioning:
  current_version: 2.1
  breaking_changes: false
  deprecation_notice: null
  compatibility: backward_compatible
```

---

#### 4. Entity Resolution and Identification
**Financial Relevance: 9/10**

**Key Skills:**
- Develop systems to uniquely identify financial entities (instruments, accounts, transactions)
- Ensure consistency across datasets
- Handle entity resolution at scale

**Real-World Challenge:**
```
Problem: Same customer appears as:
- "John A. Smith" (CRM)
- "J. Smith" (Trading Platform)  
- "Smith, John Andrew" (KYC System)
- Customer ID: 12345, 12346, 12347 (duplicates)

Solution Approach:
1. Canonical identifier (Golden Record)
2. Fuzzy matching algorithms
3. Master Data Management (MDM)
4. Match scoring and confidence thresholds
```

**SQL Example (Fuzzy Matching):**
```sql
-- Snowflake fuzzy matching for entity resolution
WITH customer_pairs AS (
    SELECT 
        a.customer_id AS id_a,
        b.customer_id AS id_b,
        a.full_name AS name_a,
        b.full_name AS name_b,
        EDITDISTANCE(UPPER(a.full_name), UPPER(b.full_name)) AS edit_dist,
        JAROWINKLER_SIMILARITY(a.email, b.email) AS email_similarity
    FROM customers a
    CROSS JOIN customers b
    WHERE a.customer_id < b.customer_id  -- Avoid duplicate pairs
)
SELECT *
FROM customer_pairs
WHERE edit_dist < 3  -- Names within 3 character edits
   OR email_similarity > 0.85
ORDER BY edit_dist, email_similarity DESC;
```

---

## 📈 Priority 2: Large-Scale Data Architecture

### Core Concepts

#### 5. Data Mesh Architecture
**Financial Relevance: 7/10**

**Key Skills:**
- Design domain-oriented, decentralized data architecture
- Implement self-serve data infrastructure
- Build data products with clear ownership

**Data Mesh Principles:**
```
1. Domain Ownership
   - Payments domain owns payment data products
   - Trading domain owns market data products
   - Each domain has dedicated data engineers

2. Data as a Product
   - Discoverable (in data catalog)
   - Addressable (APIs, query interfaces)
   - Trustworthy (SLAs, quality metrics)
   - Self-describing (metadata, documentation)

3. Self-Serve Data Platform
   - Automated data pipeline provisioning
   - Standard governance policies
   - Monitoring and observability tools

4. Federated Computational Governance
   - Global policies (security, privacy, compliance)
   - Domain autonomy within guardrails
   - Automated policy enforcement
```

**Interview Question:**
> "How would you implement Data Mesh for a financial institution with 50+ applications?"

**Answer Structure:**
1. Identify domains (payments, loans, investments, customer, risk)
2. Define data products per domain
3. Establish data contracts between domains
4. Implement central data catalog (discovery)
5. Automated governance enforcement (policies as code)
6. Federated access control (domain-level permissions)

---

#### 6. Enterprise Data Catalog
**Financial Relevance: 6/10**

**Key Skills:**
- Implement data discovery and search capabilities
- Organize data into logical domains
- Manage metadata for enhanced searchability

**Catalog Structure:**
```
Enterprise Data Catalog
│
├── Domains
│   ├── Customer Data
│   │   ├── customer_master (source: CRM)
│   │   ├── customer_transactions (source: Core Banking)
│   │   └── customer_risk_scores (source: Risk Analytics)
│   │
│   ├── Market Data
│   │   ├── equity_prices (source: Bloomberg)
│   │   ├── fx_rates (source: Reuters)
│   │   └── bond_yields (source: Internal)
│   │
│   └── Regulatory Reporting
│       ├── sox_controls (source: Finance)
│       └── aml_reports (source: Compliance)
│
├── Metadata
│   ├── Business Glossary
│   ├── Technical Metadata (schemas, types)
│   ├── Operational Metadata (lineage, quality)
│   └── Sensitivity Classification (PII, Confidential)
│
└── Access & Governance
    ├── Data Stewards (by domain)
    ├── Access Policies (RBAC)
    └── Quality SLAs
```

---

#### 7. Streaming Data and Real-Time Processing
**Financial Relevance: 8/10**

**Key Skills:**
- Handle continuous data streams (transactions, market data)
- Manage out-of-order and duplicate events
- Build materialized views for real-time analytics

**Use Cases in Finance:**
```
1. Fraud Detection
   - Real-time transaction screening
   - Anomaly detection within seconds
   - Immediate alerts and blocking

2. Market Data Processing
   - High-frequency trading signals
   - Risk calculations (Value at Risk)
   - Portfolio rebalancing triggers

3. Regulatory Compliance
   - Trade surveillance
   - Transaction reporting (MiFID II)
   - Suspicious activity monitoring (AML)
```

**Streaming Architecture Example:**
```
Data Sources → Kafka Topics → Stream Processors → Materialized Views → Applications
     ↓              ↓                ↓                    ↓
Transactions   enrichment    deduplication         dashboards
Market Data    validation    aggregation          alerts  
Events         filtering     windowing            reports
```

**Python Example (Conceptual):**
```python
# Streaming fraud detection pipeline
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Real-time fraud rules
def check_fraud(transaction):
    fraud_flags = []
    
    # Rule 1: Amount threshold
    if transaction['amount'] > 10000:
        fraud_flags.append('high_amount')
    
    # Rule 2: Velocity check (would query recent history)
    # if count_recent_transactions(account, minutes=5) > 10:
    #     fraud_flags.append('high_velocity')
    
    # Rule 3: Geographic anomaly
    # if unusual_location(transaction['location'], account_history):
    #     fraud_flags.append('geo_anomaly')
    
    return {
        'transaction_id': transaction['id'],
        'fraud_score': len(fraud_flags) / 3.0,
        'flags': fraud_flags,
        'action': 'block' if len(fraud_flags) >= 2 else 'allow'
    }

for message in consumer:
    txn = message.value
    result = check_fraud(txn)
    
    if result['action'] == 'block':
        # Send to fraud investigation queue
        print(f"🚨 BLOCKED: {txn['id']} - {result['flags']}")
    
    # Log for audit trail (governance requirement)
    log_decision(txn, result)
```

---

## 🤖 Priority 3: AI/ML Integration with Governance

#### 8. ML Model Governance
**Financial Relevance: 8/10**

**Key Challenges:**
- Model explainability (regulatory requirement)
- Data provenance for training datasets
- Bias detection and mitigation
- Model versioning and lineage
- Performance monitoring in production

**Governance Framework for ML:**
```yaml
model_governance:
  model_id: credit_risk_model_v3
  
  data_governance:
    training_data:
      - dataset: "customer_transactions_2020_2024"
        records: 5_000_000
        pii_handling: "tokenized"
        lineage: "documented in catalog"
        bias_analysis: "completed 2025-11-01"
    
    feature_store:
      platform: "Feast / Snowflake"
      features:
        - credit_score (source: Experian)
        - debt_to_income_ratio (source: Internal)
        - employment_history (source: HR System)
      access_control: "feature-level RBAC"
  
  model_governance:
    algorithm: "XGBoost"
    hyperparameters: "logged in MLflow"
    explainability:
      method: "SHAP values"
      documentation: "available in model registry"
    
    fairness_metrics:
      demographic_parity: 0.92
      equal_opportunity: 0.89
      disparate_impact_ratio: 0.85
      bias_mitigation: "reweighing applied"
    
    performance_monitoring:
      accuracy: 0.87
      precision: 0.84
      recall: 0.82
      monitoring_frequency: "daily"
      drift_detection: "enabled"
      alert_thresholds: "accuracy < 0.80"
  
  compliance:
    regulations: ["FCRA", "ECOA", "Fair Lending"]
    audit_trail: "enabled"
    model_documentation: "completed"
    approval_status: "approved by Model Risk Management"
    review_frequency: "quarterly"
```

---

#### 9. Microsoft Agent Framework (Your Recent Work!)

**Key Skills:**
- Multi-agent orchestration for data workflows
- Azure AI integration for managed services
- State management and checkpointing
- Asynchronous processing at scale

**Financial Use Case: Automated Compliance Reporting**
```python
import asyncio
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

# Multi-agent system for regulatory reporting
async def generate_compliance_report(report_date: str):
    """
    Orchestrate multiple AI agents to generate comprehensive compliance report
    """
    chat_client = AzureOpenAIChatClient(credential=AzureCliCredential())
    
    async with (
        # Agent 1: Data extraction from various sources
        ChatAgent(
            chat_client=chat_client,
            instructions="Extract transaction data for regulatory reporting. "
                        "Ensure all required fields per MiFID II are present.",
            name="DataExtractor"
        ) as extractor,
        
        # Agent 2: Data quality validation
        ChatAgent(
            chat_client=chat_client,
            instructions="Validate data quality: completeness, accuracy, timeliness. "
                        "Flag any records failing validation rules.",
            name="QualityValidator"
        ) as validator,
        
        # Agent 3: Regulatory calculations
        ChatAgent(
            chat_client=chat_client,
            instructions="Calculate regulatory metrics: capital ratios, "
                        "liquidity coverage, risk-weighted assets.",
            name="RegulatoryCalculator"
        ) as calculator,
        
        # Agent 4: Report generation
        ChatAgent(
            chat_client=chat_client,
            instructions="Generate formatted regulatory report with executive summary, "
                        "detailed tables, and compliance attestations.",
            name="ReportGenerator"
        ) as reporter
    ):
        # Sequential workflow
        print(f"🔍 Extracting data for {report_date}...")
        raw_data = await extractor.run(
            f"Extract all transactions for {report_date} from data warehouse"
        )
        
        print(f"✅ Validating data quality...")
        validated = await validator.run(
            f"Validate this dataset: {raw_data.text[:500]}..."
        )
        
        print(f"🧮 Calculating regulatory metrics...")
        metrics = await calculator.run(
            f"Calculate required metrics from: {validated.text[:500]}..."
        )
        
        print(f"📄 Generating final report...")
        final_report = await reporter.run(
            f"Create compliance report with metrics: {metrics.text}"
        )
        
        return final_report.text

# Run the compliance workflow
report = asyncio.run(generate_compliance_report("2025-11-22"))
print(report)
```

**Governance Integration:**
- **Audit Trail**: Every agent action logged
- **Data Lineage**: Track data flow through agents
- **Version Control**: Agent instructions versioned
- **Access Control**: Azure AD integration
- **Checkpointing**: Resume on failure (critical for long reports)

---

## 🔧 Priority 4: Technical Skills (SQL, Python, Cloud)

### Snowflake SQL for Financial Data

#### Window Functions for Time-Series Analysis
```sql
-- Calculate running totals and moving averages for portfolio
SELECT 
    trade_date,
    symbol,
    close_price,
    volume,
    
    -- Running total of volume
    SUM(volume) OVER (
        PARTITION BY symbol 
        ORDER BY trade_date
        ROWS UNBOUNDED PRECEDING
    ) AS cumulative_volume,
    
    -- 30-day moving average
    AVG(close_price) OVER (
        PARTITION BY symbol
        ORDER BY trade_date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS moving_avg_30d,
    
    -- Volatility (stddev over 30 days)
    STDDEV(close_price) OVER (
        PARTITION BY symbol
        ORDER BY trade_date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS volatility_30d,
    
    -- Rank by volume within each day
    RANK() OVER (
        PARTITION BY trade_date
        ORDER BY volume DESC
    ) AS volume_rank
    
FROM market_data
WHERE trade_date >= '2025-01-01'
ORDER BY symbol, trade_date;
```

#### Data Quality Checks in SQL
```sql
-- Comprehensive data quality assessment
WITH quality_checks AS (
    SELECT 
        'transactions' AS table_name,
        COUNT(*) AS total_records,
        
        -- Completeness checks
        COUNT(*) - COUNT(transaction_id) AS missing_txn_id,
        COUNT(*) - COUNT(account_number) AS missing_account,
        COUNT(*) - COUNT(amount) AS missing_amount,
        
        -- Validity checks
        SUM(CASE WHEN amount <= 0 THEN 1 ELSE 0 END) AS negative_amounts,
        SUM(CASE WHEN transaction_date > CURRENT_DATE THEN 1 ELSE 0 END) AS future_dates,
        
        -- Uniqueness checks
        COUNT(*) - COUNT(DISTINCT transaction_id) AS duplicate_txn_ids,
        
        -- Timeliness
        DATEDIFF('hour', MAX(transaction_date), CURRENT_TIMESTAMP) AS hours_since_latest,
        
        -- Calculate quality score
        (
            1.0 - (
                (COUNT(*) - COUNT(transaction_id)) + 
                (COUNT(*) - COUNT(account_number)) +
                SUM(CASE WHEN amount <= 0 THEN 1 ELSE 0 END)
            ) * 1.0 / COUNT(*)
        ) * 100 AS quality_score_pct
        
    FROM transactions
    WHERE transaction_date >= CURRENT_DATE - 7  -- Last 7 days
)
SELECT 
    *,
    CASE 
        WHEN quality_score_pct >= 99.5 THEN 'EXCELLENT'
        WHEN quality_score_pct >= 95.0 THEN 'GOOD'
        WHEN quality_score_pct >= 90.0 THEN 'FAIR'
        ELSE 'POOR'
    END AS quality_rating
FROM quality_checks;
```

#### Implementing Data Contracts in Snowflake
```sql
-- Create table with governance metadata
CREATE OR REPLACE TABLE customer_transactions (
    transaction_id VARCHAR(50) NOT NULL COMMENT 'Unique transaction identifier',
    account_number VARCHAR(20) NOT NULL COMMENT 'PII: Customer account - tokenized',
    customer_ssn VARCHAR(11) COMMENT 'PII: SSN - encrypted with AES-256',
    amount DECIMAL(18,2) NOT NULL CHECK (amount > 0) COMMENT 'Transaction amount in USD',
    transaction_date TIMESTAMP_NTZ NOT NULL COMMENT 'Transaction timestamp in UTC',
    transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('DEPOSIT', 'WITHDRAWAL', 'TRANSFER')),
    
    -- Metadata columns
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    created_by VARCHAR(100) DEFAULT CURRENT_USER(),
    data_classification VARCHAR(20) DEFAULT 'CONFIDENTIAL',
    
    -- Constraints
    PRIMARY KEY (transaction_id),
    CHECK (transaction_date <= CURRENT_TIMESTAMP())  -- No future dates
)
COMMENT = 'Customer transactions - SOX controlled, 7-year retention, daily backup'
DATA_RETENTION_TIME_IN_DAYS = 2555  -- 7 years for SOX
;

-- Row-level security for PII protection
CREATE OR REPLACE ROW ACCESS POLICY txn_access_policy
AS (user_role VARCHAR) RETURNS BOOLEAN ->
    CASE
        WHEN CURRENT_ROLE() IN ('COMPLIANCE_ADMIN', 'AUDITOR') THEN TRUE
        WHEN CURRENT_ROLE() = 'ANALYST' AND user_role = 'MASKED' THEN TRUE
        ELSE FALSE
    END
;

-- Apply policy
ALTER TABLE customer_transactions 
    ADD ROW ACCESS POLICY txn_access_policy ON (data_classification);

-- Tag for governance
CREATE TAG pii_tag ALLOWED_VALUES 'high', 'medium', 'low';
ALTER TABLE customer_transactions 
    MODIFY COLUMN customer_ssn SET TAG pii_tag = 'high';
ALTER TABLE customer_transactions 
    MODIFY COLUMN account_number SET TAG pii_tag = 'medium';
```

---

### Python for Data Quality and ETL

#### Data Validation Framework
```python
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import pandas as pd

@dataclass
class ValidationRule:
    """Define a data quality validation rule"""
    name: str
    column: str
    rule_type: str  # 'not_null', 'range', 'format', 'unique'
    parameters: Dict[str, Any]
    severity: str = 'error'  # 'error', 'warning', 'info'

@dataclass
class ValidationResult:
    """Results of validation"""
    rule_name: str
    passed: bool
    failed_count: int
    failed_percentage: float
    severity: str
    details: str

class DataQualityValidator:
    """Comprehensive data quality validation framework"""
    
    def __init__(self, rules: List[ValidationRule]):
        self.rules = rules
        self.results: List[ValidationResult] = []
    
    def validate(self, df: pd.DataFrame) -> List[ValidationResult]:
        """Run all validation rules"""
        self.results = []
        
        for rule in self.rules:
            if rule.rule_type == 'not_null':
                result = self._check_not_null(df, rule)
            elif rule.rule_type == 'range':
                result = self._check_range(df, rule)
            elif rule.rule_type == 'format':
                result = self._check_format(df, rule)
            elif rule.rule_type == 'unique':
                result = self._check_unique(df, rule)
            else:
                continue
            
            self.results.append(result)
        
        return self.results
    
    def _check_not_null(self, df: pd.DataFrame, rule: ValidationRule) -> ValidationResult:
        """Check for null values"""
        null_count = df[rule.column].isnull().sum()
        total = len(df)
        
        return ValidationResult(
            rule_name=rule.name,
            passed=(null_count == 0),
            failed_count=null_count,
            failed_percentage=(null_count / total * 100) if total > 0 else 0,
            severity=rule.severity,
            details=f"Found {null_count} null values in {rule.column}"
        )
    
    def _check_range(self, df: pd.DataFrame, rule: ValidationRule) -> ValidationResult:
        """Check if values are within acceptable range"""
        min_val = rule.parameters.get('min')
        max_val = rule.parameters.get('max')
        
        mask = (df[rule.column] >= min_val) & (df[rule.column] <= max_val)
        failed_count = (~mask).sum()
        total = len(df)
        
        return ValidationResult(
            rule_name=rule.name,
            passed=(failed_count == 0),
            failed_count=failed_count,
            failed_percentage=(failed_count / total * 100) if total > 0 else 0,
            severity=rule.severity,
            details=f"{failed_count} values outside range [{min_val}, {max_val}]"
        )
    
    def _check_format(self, df: pd.DataFrame, rule: ValidationRule) -> ValidationResult:
        """Check if values match expected format (regex)"""
        import re
        pattern = rule.parameters.get('pattern')
        
        mask = df[rule.column].astype(str).str.match(pattern, na=False)
        failed_count = (~mask).sum()
        total = len(df)
        
        return ValidationResult(
            rule_name=rule.name,
            passed=(failed_count == 0),
            failed_count=failed_count,
            failed_percentage=(failed_count / total * 100) if total > 0 else 0,
            severity=rule.severity,
            details=f"{failed_count} values don't match pattern {pattern}"
        )
    
    def _check_unique(self, df: pd.DataFrame, rule: ValidationRule) -> ValidationResult:
        """Check for duplicate values"""
        duplicate_count = df[rule.column].duplicated().sum()
        total = len(df)
        
        return ValidationResult(
            rule_name=rule.name,
            passed=(duplicate_count == 0),
            failed_count=duplicate_count,
            failed_percentage=(duplicate_count / total * 100) if total > 0 else 0,
            severity=rule.severity,
            details=f"Found {duplicate_count} duplicate values in {rule.column}"
        )
    
    def generate_report(self) -> str:
        """Generate human-readable validation report"""
        report = ["=" * 60]
        report.append("DATA QUALITY VALIDATION REPORT")
        report.append(f"Timestamp: {datetime.now().isoformat()}")
        report.append("=" * 60)
        
        total_rules = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        
        report.append(f"\nSummary: {passed}/{total_rules} rules passed")
        report.append("\nDetailed Results:")
        report.append("-" * 60)
        
        for result in self.results:
            status = "✅ PASS" if result.passed else f"❌ FAIL ({result.severity.upper()})"
            report.append(f"\n{status} - {result.rule_name}")
            report.append(f"  {result.details}")
            if not result.passed:
                report.append(f"  Failed: {result.failed_count} records ({result.failed_percentage:.2f}%)")
        
        return "\n".join(report)


# Example usage for financial transactions
if __name__ == "__main__":
    # Define validation rules
    rules = [
        ValidationRule(
            name="Transaction ID Required",
            column="transaction_id",
            rule_type="not_null",
            parameters={},
            severity="error"
        ),
        ValidationRule(
            name="Amount Must Be Positive",
            column="amount",
            rule_type="range",
            parameters={"min": 0.01, "max": 1_000_000.00},
            severity="error"
        ),
        ValidationRule(
            name="Account Number Format",
            column="account_number",
            rule_type="format",
            parameters={"pattern": r"^\d{10,12}$"},
            severity="error"
        ),
        ValidationRule(
            name="Transaction ID Uniqueness",
            column="transaction_id",
            rule_type="unique",
            parameters={},
            severity="error"
        ),
    ]
    
    # Sample data
    df = pd.DataFrame({
        'transaction_id': ['TXN001', 'TXN002', 'TXN003', None, 'TXN002'],  # Has null and duplicate
        'amount': [100.50, -50.00, 200.00, 150.00, 75.00],  # Has negative
        'account_number': ['1234567890', '9876543210', 'invalid', '1122334455', '5566778899']  # Has invalid format
    })
    
    # Run validation
    validator = DataQualityValidator(rules)
    results = validator.validate(df)
    
    # Print report
    print(validator.generate_report())
```

---

## 📚 Key Topics Summary for Interview Prep

### Must-Know Concepts (Memorize These!)

#### 1. **Data Governance Pillars**
```
✓ Data Quality: Accuracy, Completeness, Consistency, Timeliness, Validity
✓ Data Security: Encryption, Access Control, Audit Logging
✓ Data Privacy: PII Protection, Consent Management, Right to Erasure
✓ Data Lineage: Source → Transform → Destination tracking
✓ Data Stewardship: Owners, Custodians, Consumers
✓ Regulatory Compliance: SOX, GDPR, FINRA, MiFID II, BCBS 239
```

#### 2. **Financial Data Characteristics**
```
✓ High Volume: Millions of transactions daily
✓ High Velocity: Real-time processing requirements
✓ High Value: Errors have financial/regulatory impact
✓ Protected: PII, account data, trading strategies
✓ Regulated: Audit trails, retention policies
✓ Complex: Multiple systems, formats, standards
```

#### 3. **Governance Implementation Patterns**
```
✓ Data Catalog: Central discovery and metadata management
✓ Data Mesh: Domain-oriented decentralized architecture
✓ Data Contracts: Explicit agreements between producers/consumers
✓ Data Quality Framework: Automated validation and monitoring
✓ Access Control: RBAC, ABAC, column/row-level security
✓ Lineage Tracking: Automated capture and visualization
```

#### 4. **Technology Stack (Common in Financial Services)**
```
✓ Cloud Platforms: Azure (most likely), AWS, GCP
✓ Data Warehouses: Snowflake, Databricks, Synapse
✓ Streaming: Kafka, Azure Event Hubs, Kinesis
✓ Orchestration: Airflow, Azure Data Factory, dbt
✓ Governance: Collibra, Alation, Purview
✓ ML Platforms: Azure ML, Databricks ML, SageMaker
```

---

## 🎤 Common Interview Questions & Answers

### Question 1: "How do you ensure data quality in a large-scale financial system?"

**Strong Answer:**
```
I implement a multi-layered data quality framework:

1. **Prevention Layer** (Source)
   - Schema validation at ingestion
   - Data contracts with upstream systems
   - Format validation and type checking

2. **Detection Layer** (Pipeline)
   - Automated quality checks (completeness, accuracy, consistency)
   - Anomaly detection for outliers
   - Reconciliation against source systems

3. **Correction Layer** (Remediation)
   - Automated fixes for known issues
   - Manual review workflows for critical data
   - Rejection and re-processing mechanisms

4. **Monitoring Layer** (Observability)
   - Quality metrics dashboards
   - SLA tracking (99.9% completeness target)
   - Alerts for quality degradation
   - Root cause analysis for failures

5. **Governance Layer** (Oversight)
   - Data stewardship assignment
   - Quality scorecards by domain
   - Regular audits and reviews

Example: For transaction data, I'd implement:
- NOT NULL checks on critical fields (transaction_id, amount, date)
- Range validation (amount > 0, date <= current_time)
- Format validation (account numbers match pattern)
- Duplicate detection (unique transaction_id)
- Timeliness checks (data arrives within SLA)
- Cross-system reconciliation (totals match source)
```

---

### Question 2: "How do you handle PII in a data pipeline for ML models?"

**Strong Answer:**
```
I follow a defense-in-depth approach for PII protection:

1. **Classification**: Tag all PII fields (SSN, account numbers, email)

2. **Minimization**: Only collect PII absolutely necessary for the use case

3. **Pseudonymization/Tokenization**: 
   - Replace PII with tokens for non-production environments
   - Use consistent tokens for same entity (entity resolution)
   - Store mapping in secure vault (Azure Key Vault)

4. **Encryption**: 
   - At rest: AES-256 encryption
   - In transit: TLS 1.3
   - Column-level encryption in Snowflake for sensitive fields

5. **Access Control**:
   - RBAC with least privilege
   - Row-level security (only see your region's data)
   - Column-level security (PII masked for analysts)
   - Audit logging of all PII access

6. **Model Training**:
   - Use tokenized data where possible
   - Feature engineering to reduce PII dependency
   - Federated learning for sensitive use cases
   - Differential privacy techniques

7. **Compliance**:
   - GDPR: Right to erasure, consent tracking
   - CCPA: Data subject access requests
   - FCRA: Adverse action notices
   - Regular privacy impact assessments

Example: For a credit scoring model:
- Tokenize SSN and account numbers
- Hash email addresses
- Use only derived features (not raw PII)
- Maintain lineage for explainability
- Log all data access for audits
```

---

### Question 3: "Explain how you'd implement data lineage for a complex financial workflow."

**Strong Answer:**
```
I implement automated data lineage tracking across the pipeline:

1. **Metadata Capture**:
   - Parse SQL queries to extract source/target tables
   - Instrument ETL jobs to log transformations
   - Capture API calls between microservices
   - Tag data assets with business context

2. **Lineage Graph Construction**:
   ```
   Source Systems → Ingestion → Staging → Transformation → Serving
        ↓              ↓           ↓             ↓            ↓
   Core Banking    Kafka      Raw Layer    Business     Dashboards
   CRM            Event Hub   Validated     Logic       ML Models
   Trading Sys    API         Cleansed      Aggregates  Reports
   ```

3. **Technical Implementation**:
   - OpenLineage standard for interoperability
   - Store in graph database (Neo4j) or data catalog (Purview)
   - Column-level lineage for sensitive fields
   - Version history for schema evolution

4. **Automated Tracking**:
   - dbt for transformation lineage (built-in)
   - Airflow DAGs capture workflow dependencies
   - Snowflake query history for runtime lineage
   - Custom decorators for Python functions

5. **Governance Integration**:
   - Impact analysis: "What breaks if I change this table?"
   - Root cause analysis: "Where did this bad data originate?"
   - Compliance: "Trace this customer's data through all systems"
   - Audit: "Prove data wasn't tampered with"

Example lineage query:
```sql
-- Find all downstream dependencies of customer_master table
WITH RECURSIVE lineage AS (
  SELECT table_name, downstream_table, 1 AS depth
  FROM lineage_graph
  WHERE table_name = 'customer_master'
  
  UNION ALL
  
  SELECT lg.table_name, lg.downstream_table, l.depth + 1
  FROM lineage_graph lg
  JOIN lineage l ON lg.table_name = l.downstream_table
  WHERE l.depth < 10  -- Prevent infinite loops
)
SELECT DISTINCT downstream_table, MIN(depth) AS min_hops
FROM lineage
GROUP BY downstream_table
ORDER BY min_hops;
```

This gives stakeholders visibility: "Customer table feeds 47 downstream assets"
```

---

### Question 4: "How would you design a data governance framework for a Data Mesh architecture?"

**Strong Answer:**
```
Data Mesh requires federated governance - global standards with domain autonomy:

1. **Centralized Governance (Global Policies)**:
   ```
   - Security: Encryption standards, access control policies
   - Privacy: PII handling, consent management
   - Compliance: Regulatory requirements (SOX, GDPR)
   - Quality: Minimum SLAs (99% completeness)
   - Metadata: Required fields (owner, classification, lineage)
   ```

2. **Decentralized Ownership (Domain Level)**:
   ```
   Payments Domain:
   - Owns: transaction_data_product
   - Steward: Payments Team Lead
   - SLA: 99.9% availability, <5 min latency
   - Access: Published API, documented schema
   
   Risk Domain:
   - Owns: risk_scores_data_product
   - Steward: Risk Analytics Manager
   - SLA: Daily refresh by 6 AM
   - Access: Snowflake share, dbt models
   ```

3. **Data Contracts**:
   ```yaml
   # Example contract between domains
   producer: payments_domain
   consumer: fraud_detection_domain
   
   schema_version: 2.1
   breaking_changes: false
   
   fields:
     - transaction_id: STRING (required, unique)
     - amount: DECIMAL(18,2) (required, > 0)
     - timestamp: TIMESTAMP_UTC (required)
   
   sla:
     availability: 99.9%
     latency: < 5 minutes
     quality: 99.5% completeness
   
   governance:
     pii_fields: [account_number, customer_id]
     access_level: CONFIDENTIAL
     retention: 7 years (SOX)
   ```

4. **Automated Policy Enforcement**:
   - Policy-as-code (OPA, Azure Policy)
   - Automated compliance checks in CI/CD
   - Data catalog enforces metadata standards
   - Access control via RBAC/ABAC

5. **Observability**:
   - Each domain publishes quality metrics
   - Central dashboard shows compliance scores
   - Automated alerts for SLA breaches
   - Regular governance reviews

6. **Self-Serve Platform**:
   - Templated data product creation
   - Automated quality checks
   - Built-in lineage tracking
   - Standard governance metadata

Success metrics:
- Time to create new data product: <1 week
- Governance compliance score: >95%
- Cross-domain data sharing: Enabled via catalog
- Audit readiness: 100% lineage coverage
```

---

## 💡 Interview Tips & Strategies

### Do's:
- ✅ Use **STAR method** (Situation, Task, Action, Result) for behavioral questions
- ✅ Relate everything back to **financial services context**
- ✅ Emphasize **compliance and risk management**
- ✅ Show understanding of **scale** (millions of records, real-time processing)
- ✅ Mention specific **tools and technologies** you've used
- ✅ Discuss **trade-offs** when proposing solutions
- ✅ Ask clarifying questions about their specific governance challenges

### Don'ts:
- ❌ Don't ignore **regulatory requirements** (they're critical in finance)
- ❌ Don't overlook **security** (encryption, access control, audit logs)
- ❌ Don't propose solutions without considering **auditability**
- ❌ Don't forget about **operational overhead** (who maintains this?)
- ❌ Don't dismiss **legacy systems** (they exist in every financial institution)

### Key Phrases to Use:
```
✓ "In my previous work extracting skills from financial data books..."
✓ "I implemented automated governance using Microsoft Agent Framework..."
✓ "We ensured GDPR compliance by implementing row-level security..."
✓ "To maintain audit trails, we logged all transformations in..."
✓ "For data lineage, we used a combination of dbt and custom tracking..."
✓ "The data quality framework reduced production issues by 80%..."
```

---

## 🔗 Additional Resources to Review

### Your Recent Work (Leverage This!)
1. **Microsoft Agent Framework skills** (`skills.md`)
   - Multi-agent orchestration
   - Azure AI integration
   - State management and checkpointing
   
2. **Data Governance Skills** (Recent extractions)
   - Enterprise Data Catalog concepts
   - Data Mesh architecture patterns
   - Financial data engineering principles

### Quick Reference Cheat Sheets
```
📋 Data Governance Checklist:
□ Data Classification (Public, Internal, Confidential, Restricted)
□ Data Ownership (Steward assigned for each domain)
□ Data Quality (SLAs defined and monitored)
□ Data Lineage (Automated tracking implemented)
□ Access Control (RBAC with least privilege)
□ Encryption (At rest and in transit)
□ Audit Logging (All access and changes tracked)
□ Compliance (SOX, GDPR, FINRA requirements met)
□ Retention Policy (7 years for financial data)
□ Disaster Recovery (Backup and restore tested)

📋 Data Quality Dimensions:
□ Accuracy: Values are correct
□ Completeness: No missing required fields
□ Consistency: Values match across systems
□ Timeliness: Data arrives within SLA
□ Validity: Values conform to business rules
□ Uniqueness: No unwanted duplicates

📋 PII Protection Checklist:
□ Identified all PII fields
□ Classified sensitivity level
□ Implemented encryption
□ Applied access controls
□ Enabled audit logging
□ Tokenization for non-prod
□ Consent tracking (if applicable)
□ Data subject access request process
```

---

## ✅ Final Preparation Checklist

### Tonight (Sunday):
- [ ] Review Priority 1: Data Governance sections
- [ ] Memorize key governance concepts and regulations
- [ ] Review your Microsoft Agent Framework code (`skills.md`)

### Monday:
- [ ] Review Priority 2: Large-Scale Architecture
- [ ] Practice explaining Data Mesh and Data Catalog
- [ ] Review SQL examples (Snowflake specific)

### Tuesday Morning (Interview Day):
- [ ] Quick review of common interview questions
- [ ] Review your recent work (skills extraction pipeline)
- [ ] Prepare 2-3 questions to ask them about their governance challenges

---

## 🎯 Your Unique Selling Points

Based on your recent work, emphasize:

1. **Hands-On AI/ML Governance**: 
   - "I built a multi-agent system using Microsoft Agent Framework to extract and validate skills from financial data books"
   - Shows: AI implementation + data quality + automation

2. **Large-Scale Data Processing**:
   - "Processed 10+ technical books, extracting 3000+ structured skill records"
   - Shows: Scale, ETL, data structuring

3. **Metadata Management**:
   - "Created comprehensive skill taxonomy with governance metadata (difficulty, prerequisites, financial relevance)"
   - Shows: Classification, metadata standards, domain knowledge

4. **Azure Expertise**:
   - "Implemented Azure OpenAI integration with proper credential management and async processing"
   - Shows: Cloud-native, security-conscious, modern architecture

5. **State Management & Reliability**:
   - "Built checkpointing system for long-running workflows to ensure resumability"
   - Shows: Production-ready thinking, fault tolerance

---

**Good luck on Tuesday! You've got this! 🚀**

Remember: They're looking for someone who understands **both the technical implementation AND the governance/compliance requirements** - and you clearly have both!
