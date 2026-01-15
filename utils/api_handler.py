import requests
import re
import os

# Task 3.1a: Fetch All Products
def fetch_all_products():
    """
    Fetches all products from DummyJSON API.
    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('products', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API data: {e}")
        return []

# Task 3.1b: Create Product Mapping
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info.
    Parameters: api_products from fetch_all_products()
    Returns: dictionary mapping product IDs to info
    """
    mapping = {}
    for p in api_products:
        p_id = p.get('id')
        if p_id:
            mapping[p_id] = {
                'title': p.get('title'),
                'category': p.get('category'),
                'brand': p.get('brand'),
                'rating': p.get('rating')
            }
    return mapping

# Task 3.2: Enrich Sales Data
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information.
    """
    enriched_data = []
    
    for t in transactions:
        # Create a copy to avoid mutating original list items in place unexpectedly
        enriched_t = t.copy()
        
        # Extract numeric ID from ProductID (e.g. "P101" -> 101)
        p_id_str = t.get('ProductID', '')
        match = re.search(r'\d+', p_id_str)
        
        extracted_id = int(match.group()) if match else None
        
        # Enrichment Logic
        api_info = product_mapping.get(extracted_id) if extracted_id else None
        
        if api_info:
            enriched_t['API_Category'] = api_info.get('category')
            enriched_t['API_Brand'] = api_info.get('brand')
            enriched_t['API_Rating'] = api_info.get('rating')
            enriched_t['API_Match'] = True
        else:
            enriched_t['API_Category'] = None
            enriched_t['API_Brand'] = None
            enriched_t['API_Rating'] = None
            enriched_t['API_Match'] = False
            
        enriched_data.append(enriched_t)
        
    return enriched_data

# Task 3.2: Save Enriched Data
def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file.
    Expected File Format: Pipe delimited, with new headers.
    """
    if not enriched_transactions:
        print("No enriched data to save.")
        return

    # Ensure output directory exists (data/ comes from filename typically, but check)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Define Column Order
    # Original: TransactionID, Date, ProductID, ProductName, Quantity, UnitPrice, CustomerID, Region
    # New: API_Category, API_Brand, API_Rating, API_Match
    
    headers = [
        'TransactionID', 'Date', 'ProductID', 'ProductName', 'Quantity', 'UnitPrice', 
        'CustomerID', 'Region', 'API_Category', 'API_Brand', 'API_Rating', 'API_Match'
    ]
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Write Header
            f.write('|'.join(headers) + '\n')
            
            for t in enriched_transactions:
                row = []
                for field in headers:
                    val = t.get(field)
                    # Handle None and types
                    if val is None:
                        row.append('') # Or 'None'? Requirement implies handling None appropriately. Empty string is common CSV/Pipe practice for null.
                    else:
                        row.append(str(val))
                f.write('|'.join(row) + '\n')
                
        print(f"Enriched data saved successfully to: {filename}")
    except Exception as e:
        print(f"Error saving enriched data: {e}")

