# Hybrid ETL Data Orchestration Pipeline

A custom Extract, Transform, Load (ETL) pipeline engineered in Python to aggregate, clean, and standardize amusement park data from heterogeneous sources (local CSVs and remote JSON APIs) into unified relational and flat-file formats.

## 1. Architectural Overview
The pipeline executes a synchronous extraction and load sequence:
1. **Local Extraction:** Reads raw amusement park records from local CSV dumps.
2. **Data Transformation:** Isolates target fields (Park, Type, Open Status, Speed) and standardizes formatting.
3. **Flat-File Loading:** Exports cleaned records into a structured output CSV.
4. **Relational Database Population:** Provisions a local SQLite database (`maneges.db`) and inserts the cleaned local data.
5. **API Integration:** Fetches remote JSON data via HTTP requests and appends it to the SQLite database.

## 2. 📂 Project Architecture
```text
.
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   ├── processed/          # Cleaned CSVs, JSONs, and SQLite DB
│   └── raw/                # Unaltered source data
└── source/
    └── etl_pipeline.py     # Core ETL execution script