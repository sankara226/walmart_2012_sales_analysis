# Enterprise Walmart ETL Pipeline & Streamlit Interactive Dashboard

This is an end-to-end, fully automated asynchronous Data Engineering pipeline that programmatically extracts raw high-velocity retail sales transactions from KaggleHub, transforms statistics using a rolling 7-day moving average framework, streams clean tabular states directly into an internal SQLite database layer, and ships executive-ready automated PDF compliance metrics and operational Streamlit applications.

## Technical Architecture Overview

- **Extraction Engine:** Scalable data consumption from target API registries (`kagglehub`).
- **Transformation Core:** Implementation of rolling lookback windows and structural trend category classifiers in `pandas`.
- **Storage Abstraction Layer:** Secure target relational database streaming into localized instances (`sqlite3`).
- **Reporting Subsystems:** Programmatic PDF assembly via `fpdf2` alongside web infrastructure via `streamlit`.

## Quick Start Workspace Execution

### 1. Build Virtual Environment Infrastructure

```bash
pip install -r requirements.txt
```
