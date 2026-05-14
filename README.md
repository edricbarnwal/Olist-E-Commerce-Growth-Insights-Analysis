

# OLIST E-COMMERCE DATA ANALYTICS

> **STATUS**: Active
> **DATASET**: Olist E-Commerce Brazilian Marketplace
> **OBJECTIVE**: Extract statistical insights, identify anomalies, and map trends

## Project Overview

This repository contains a data pipeline and exploratory data analysis (EDA) framework for the Olist E-Commerce dataset. The project enforces separation between data processing, analytical reporting, and visualization generation.

### Directory Structure

```text
📦 E-Commerce Olist Dataset
├── 📂 assets/              # Visualization outputs
├── 📂 data/                
│   ├── 📂 raw/             # Source CSV files
│   └── 📂 processed/       # Aggregated analytical data
├── 📂 src/                 
│   ├── clean_data.py       # ETL & data cleaning
│   └── visualize.py        # Visualization generation
└── 📄 README.md            # Documentation
```

---

## Getting Started

### 1. Run ETL Pipeline

Cleans raw data, handles missing values, computes logistics metrics, and outputs `master_analytical_dataset.csv`.

```bash
python src/clean_data.py
```

**Expected Output:**
```
[*] Starting data cleaning pipeline...
[*] Loading raw data from data/raw...
[*] Converting datetime columns...
[*] Translating product categories...
[*] Computing logistics performance metrics...
[*] Merging master analytical dataset...
[*] Saving master processed dataset (99441 rows) to data/processed...
[+] Data cleaning complete. Outputs saved successfully.
```

### 2. Generate Visualizations

Loads processed data and generates visualization assets.

```bash
python src/visualize.py
```

---

## Key Findings

### Critical Metrics

| Metric | Value |
|--------|-------|
| Total Orders | 99,441 |
| Total Revenue | R$ 13,591,643.70 |
| Repeat Purchase Rate | 3.12% |

### Major Insights

**Retention Issue**: The 3.12% repeat rate is below industry standard (20-30%), indicating heavy reliance on single-use customer acquisition with weak lifetime value.

**Order Volume Trend**: Positive growth trajectory with significant Q4 spikes during Black Friday events.

**Revenue by Category**: Health & Beauty and Watches & Gifts drive highest revenue. High-ticket items outpace volume-driven categories.

**Geographic Concentration**: São Paulo dominates customer base, with heavy southeast concentration. Northern regions present expansion opportunities.

**Logistics Impact**: Late deliveries significantly reduce review scores from 4.21 to 2.57, making delivery performance critical to retention.

---

