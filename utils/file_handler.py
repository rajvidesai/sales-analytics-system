import os #helps check if a file exists on your computer.

# Task 1.1 read file with encoding handling
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    
    Args:
        filename (str): Path to the file.
        
    Returns:
        list: List of raw lines (strings).
    """
    if not os.path.exists(filename): #checks if the file is actually there
        print(f"Error: File not found at {filename}")
        return []

    encodings = ['utf-8', 'latin-1', 'cp1252']
    lines = []
    
    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as f:
                lines = f.readlines()
            break # Success
        except UnicodeDecodeError:
            continue
    else:
        # If loop completes without break
        print(f"Error: Could not decode file with any of the attempted encodings: {encodings}")
        return []

    # Filter empty lines
    non_empty_lines = [line.strip() for line in lines if line.strip()]

    if non_empty_lines and "TransactionID" in non_empty_lines[0]:
        return non_empty_lines[1:]
        
    return non_empty_lines

# Task 1.2
def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries.
    """
    parsed_data = []
    
    for line in raw_lines:
        parts = line.split('|')
        
        # Skip rows with incorrect number of fields
        # Expecting 8 fields based on sample
        if len(parts) < 8:
            continue
            
        # Extract fields
        # T001 | 2024-12-01 | P101 | Laptop|2|45000|C001| North
        t_id = parts[0].strip()
        date = parts[1].strip()
        p_id = parts[2].strip()
        p_name = parts[3].strip()
        qty_str = parts[4].strip()
        price_str = parts[5].strip()
        c_id = parts[6].strip()
        region = parts[7].strip()
        
        # Handle commas in ProductName (remove or replace)
        p_name = p_name.replace(',', '')
        
        # Handle commas in numeric fields
        try:
            qty = int(qty_str.replace(',', ''))
            price = float(price_str.replace(',', ''))
        except ValueError:
            # If conversion fails, valid data types requirement not met, validness depends on "Expected Valid records".
                    continue
        #Creates a clean key-value dictionary for the row and adds it to the main list.    
        record = {
            'TransactionID': t_id,
            'Date': date,
            'ProductID': p_id,
            'ProductName': p_name,
            'Quantity': qty,
            'UnitPrice': price,
            'CustomerID': c_id,
            'Region': region
        }
        parsed_data.append(record)
        
    return parsed_data 
    

# Task 1.3
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    
    Returns: tuple (valid_transactions, invalid_count, filter_summary)
    """
    valid_transactions = []
    invalid_count = 0
    
    # 1. Validation Logic
    for t in transactions:
        is_valid = True
        
        # Rules
        # Quantity must be > 0
        if t['Quantity'] <= 0:
            is_valid = False
        # UnitPrice must be > 0
        elif t['UnitPrice'] <= 0:
            is_valid = False
        # All required fields must be present 
        # Let's check string fields for emptiness
        elif not t['TransactionID'] or not t['Date'] or not t['ProductID'] or not t['ProductName'] or not t['CustomerID'] or not t['Region']:
            is_valid = False
        # TransactionID must start with 'T'
        elif not t['TransactionID'].startswith('T'):
            is_valid = False
        # ProductID must start with 'P'
        elif not t['ProductID'].startswith('P'):
            is_valid = False
        # CustomerID must start with 'C'
        elif not t['CustomerID'].startswith('C'):
            is_valid = False
            
        if is_valid:
            valid_transactions.append(t)
        else:
            invalid_count += 1
            
    # 2. Collect Info for Filter Display
    unique_regions = sorted(list(set(t['Region'] for t in valid_transactions)))
    
    # Calculate amounts for display
    amounts = [t['Quantity'] * t['UnitPrice'] for t in valid_transactions]
    if amounts:
        global_min = min(amounts)
        global_max = max(amounts)
    else:
        global_min = 0
        global_max = 0
        
    print(f"\n[Data Stats]")
    print(f"Available Regions: {unique_regions}")
    print(f"Transaction Amount Range: ${global_min:,.2f} - ${global_max:,.2f}")
    
    # 3. Filtering
    filtered_transactions = []
    
    count_input = len(transactions) # Number of rows in the input file
    
    filtered_by_region_count = 0
    filtered_by_amount_count = 0
    
    for t in valid_transactions:
        keep = True
        amount = t['Quantity'] * t['UnitPrice']
        
        if region and t['Region'] != region:
            keep = False
            filtered_by_region_count += 1
        
            
        if keep:
            if min_amount is not None and amount < min_amount:
                keep = False
                filtered_by_amount_count += 1
            elif max_amount is not None and amount > max_amount:
                keep = False
                filtered_by_amount_count += 1
        
        if keep:
            filtered_transactions.append(t)
            
    summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region_count,
        'filtered_by_amount': filtered_by_amount_count,
        'final_count': len(filtered_transactions)
    }
    
    return filtered_transactions, invalid_count, summary

