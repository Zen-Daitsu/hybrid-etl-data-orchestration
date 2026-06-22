# Hybrid ETL Data Orchestration Pipeline

A custom Extract, Transform, Load (ETL) pipeline engineered in Python to aggregate, clean, and standardize amusement park data from heterogeneous sources (local CSVs and remote JSON APIs) into unified relational and flat-file formats.

## 1. Architectural Overview
The pipeline executes a synchronous 5-stage orchestration graph:

1. **Local Extraction:** Reads raw amusement park records from local CSV dumps.
2. **Data Transformation:** Isolates target fields (Park, Type, Open Status, Speed) and standardizes formatting.
3. **Flat-File Loading:** Exports cleaned records into a structured output CSV.
4. **Relational Database Population:** Provisions a local SQLite database (`maneges.db`) and inserts the cleaned local data.
5. **API Integration:** Fetches remote JSON data via HTTP requests and appends it to the SQLite database.

## 2. Engineering Highlights & Trade-offs
* **Modular ETL Design:** Isolated extraction, transformation, and loading functions to enforce strict maintainability and code clarity.
* **Dynamic Pathing Rigor:** Leveraged native `os` module for absolute path resolution, ensuring execution stability and preventing database generation outside of designated directory zones.
* **Heterogeneous Data Handling:** Seamlessly unifies flat-file (CSV) structural processing with remote document (JSON) deserialization into a single relational schema.

## 3. Technical Stack
* **Core Language:** Python 3.x
* **Data Processing:** Native `csv` and `json` libraries
* **Relational Storage:** SQLite3
* **Network Requests:** `requests`
* **Infrastructure Target:** Cross-platform local execution

## 4. Project Architecture
```text
.
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   ├── processed/
│   └── raw/
└── source/
    └── etl_pipeline.py
```
## 5. Local Deployment & Setup

### Prerequisites
Ensure your local machine has Python 3.x installed.

### Installation
1. Clone the project locally:
   ```bash
   git clone git@github.com:Zen-Daitsu/hybrid-etl-data-orchestration.git
   cd hybrid-etl-data-orchestration
