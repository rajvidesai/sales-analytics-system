# Sales Analytics System

## Project Overview
The **Sales Analytics System** is a comprehensive data processing application designed to ingest, clean, analyze, and enrich sales transaction records. This tool serves as an end-to-end pipeline that transforms raw, messy data into actionable business insights.

### What It Does
1.  **Ingestion & Cleaning**: Reading raw transaction logs (handling encoding errors and messy formatting), validating data integrity, and filtering out corrupted records.
2.  **Advanced Analytics**: Computing key performance indicators (KPIs) such as total revenue, region-wise performance, and daily sales trends.
3.  **Data Enrichment**: Integrating with external APIs (DummyJSON) to fetch additional product details (categories, brands, ratings) that are missing from the raw sales data.
4.  **Reporting**: Automatically generating a human-readable summary report (`sales_report.txt`) containing all analysis results, top performers, and enriched data statistics.

This system is built to be modular, robust, and easily extensible for future data sources.

## Features
- **Data Cleaning**: Parses messy pipe-delimited files, handles encoding issues, and validates records.
- **API Integration**: Fetches real-time product data from [DummyJSON] (https://dummyjson.com/products).
- **Analysis**: Calculates total revenue, identifies top-selling products, and breaks down sales by region.
- **Reporting**: Generates a clear text-based report in any `output` directory.

## File Structure
```
sales-analytics-system/
├── data/
│   └── sales_data.txt      # Input data file
├── output/
│   └── sales_report.txt    # Generated report (created after running)
├── utils/
│   ├── __init__.py
│   ├── api_handler.py      # Handles API requests
│   ├── data_processor.py   # Analysis and        reporting logic
│   └── file_handler.py     # File reading and cleaning logic
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies
└── README.md               # This file
```

## Setup & Usage

### 1. Prerequisites
- **Python 3.8+** must be installed on your system.

### 2. Set Up a Virtual Environment (Recommended)
It is best practice to use a virtual environment to avoid conflicts with other projects.

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
*(You will see `(.venv)` appear in your terminal prompt when activated)*

### 3. Install Dependencies
Once your environment is active, install the required libraries:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Make sure you are in the project root directory (`sales-analytics-system/`), then execute:
```bash
python main.py
```

### 3. Check Output
The cleaning statistics will be printed to the console. The final report will be generated at `output/sales_report.txt`.

## Validation Logic
- **Invalid Records**: Records with missing IDs, negative prices/quantities, or malformed rows are removed.
- **Cleaning**: Commas are stripped from numeric fields and product names.
- **Encoding**: Handles non-UTF-8 characters (Latin-1).
