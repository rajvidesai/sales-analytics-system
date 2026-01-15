# Sales Analytics System

A Python-based system to process sales data, integrate with external APIs, analyze trends, and generate reports.

## Features
- **Data Cleaning**: Parses messy pipe-delimited files, handles encoding issues, and validates records.
- **API Integration**: Fetches real-time product data from [FakeStoreAPI](https://fakestoreapi.com/products).
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
│   ├── data_processor.py   # Analysis and reporting logic
│   └── file_handler.py     # File reading and cleaning logic
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies
└── README.md               # This file
```

## Setup & Usage

### 1. Install Dependencies
Ensure you have Python installed. Then run:
```bash
pip install -r requirements.txt
```

### 2. Run the Application
Execute the main script from the project root:
```bash
python main.py
```

### 3. Check Output
The cleaning statistics will be printed to the console. The final report will be generated at `output/sales_report.txt`.

## Validation Logic
- **Invalid Records**: Records with missing IDs, negative prices/quantities, or malformed rows are removed.
- **Cleaning**: Commas are stripped from numeric fields and product names.
- **Encoding**: Handles non-UTF-8 characters (Latin-1).
