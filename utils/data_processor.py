import os
from datetime import datetime

# ==========================================
# Task 2: Data Processing
# ==========================================

# Task 2.1a: Calculate Total Revenue
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions.
    Returns: float
    """
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)

# Task 2.1b: Region-wise Sales Analysis
def region_wise_sales(transactions):
    """
    Analyzes sales by region.
    Returns: dictionary with region statistics
    """
    total_revenue = calculate_total_revenue(transactions)
    region_stats = {}
    
    # Aggregation
    for t in transactions:
        r = t['Region']
        amount = t['Quantity'] * t['UnitPrice']
        
        if r not in region_stats:
            region_stats[r] = {'total_sales': 0.0, 'transaction_count': 0}
        
        region_stats[r]['total_sales'] += amount
        region_stats[r]['transaction_count'] += 1
        
    # Calculate percentage and format
    final_stats = {}
    for r, stats in region_stats.items():
        stats['percentage'] = round((stats['total_sales'] / total_revenue) * 100, 2) if total_revenue > 0 else 0
        final_stats[r] = stats

    # Helper to sort by total_sales descending for display logic later if needed
    # But function returns a dict. Sorting usually happens when accessing or converting to list.
    return final_stats

# Task 2.1c: Top Selling Products
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold.
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """
    product_stats = {}
    
    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']
        
        if name not in product_stats:
            product_stats[name] = {'qty': 0, 'revenue': 0.0}
            
        product_stats[name]['qty'] += qty
        product_stats[name]['revenue'] += revenue
        
    # Convert to list of tuples
    product_list = [
        (name, stats['qty'], stats['revenue']) 
        for name, stats in product_stats.items()
    ]
    
    # Sort by TotalQuantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)
    
    return product_list[:n]

# Task 2.1d: Customer Purchase Analysis
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns.
    Returns: dictionary of customer statistics
    """
    customer_stats = {}
    
    for t in transactions:
        c_id = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        product = t['ProductName']
        
        if c_id not in customer_stats:
            customer_stats[c_id] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }
            
        customer_stats[c_id]['total_spent'] += amount
        customer_stats[c_id]['purchase_count'] += 1
        customer_stats[c_id]['products_bought'].add(product)
        
    # Finalize stats (avg value, list conversion)
    final_stats = {}
    sorted_customers = sorted(customer_stats.items(), key=lambda x: x[1]['total_spent'], reverse=True)
    
    for c_id, stats in sorted_customers:
        final_stats[c_id] = {
            'total_spent': stats['total_spent'],
            'purchase_count': stats['purchase_count'],
            'avg_order_value': round(stats['total_spent'] / stats['purchase_count'], 2),
            'products_bought': list(stats['products_bought'])
        }
        
    return final_stats

# Task 2.2a: Daily Sales Trend
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date.
    Returns: dictionary sorted by date
    """
    daily_stats = {}
    
    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']
        c_id = t['CustomerID']
        
        if date not in daily_stats:
            daily_stats[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers': set()
            }
            
        daily_stats[date]['revenue'] += amount
        daily_stats[date]['transaction_count'] += 1
        daily_stats[date]['customers'].add(c_id)
        
    # Sort chronologically
    sorted_dates = sorted(daily_stats.keys())
    final_stats = {}
    
    for date in sorted_dates:
        stats = daily_stats[date]
        final_stats[date] = {
            'revenue': stats['revenue'],
            'transaction_count': stats['transaction_count'],
            'unique_customers': len(stats['customers'])
        }
        
    return final_stats

# Task 2.2b: Find Peak Sales Day
def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue.
    Returns: tuple (date, revenue, transaction_count)
    """
    trends = daily_sales_trend(transactions)
    if not trends:
        return (None, 0.0, 0)
        
    peak_date = max(trends.items(), key=lambda x: x[1]['revenue'])
    return (peak_date[0], peak_date[1]['revenue'], peak_date[1]['transaction_count'])

# Task 2.3a: Low Performing Products
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales (quantity < threshold).
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """
    # Reuse top_selling logic to get aggregated stats, but get all
    all_products = top_selling_products(transactions, n=len(transactions))
    
    low_performers = [p for p in all_products if p[1] < threshold]
    
    # Sort by TotalQuantity ascending
    low_performers.sort(key=lambda x: x[1])
    
    return low_performers

# ==========================================
# Task 4: Report Generation
# ==========================================

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report.
    """
    # Calculate all stats
    total_revenue = calculate_total_revenue(transactions)
    total_txns = len(transactions)
    avg_order_val = total_revenue / total_txns if total_txns > 0 else 0
    
    dates = sorted([t['Date'] for t in transactions])
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"
    
    region_stats = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, n=5)
    customer_stats = customer_analysis(transactions)
    daily_trends = daily_sales_trend(transactions)
    
    peak_day = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions, threshold=5) # Example threshold
    
    # API Enrichment Stats
    # Assuming 'API_Match' might be in enriched_transactions
    # If enriched_transactions is passed, calculate stats from it
    # If not, use empty defaults
    total_enriched = len(enriched_transactions)
    successful_enrichment = sum(1 for t in enriched_transactions if t.get('API_Match') is True)
    success_rate = (successful_enrichment / total_enriched * 100) if total_enriched > 0 else 0.0
    missing_products = list(set(t['ProductName'] for t in enriched_transactions if t.get('API_Match') is False))

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # 1. HEADER
        f.write("SALES ANALYTICS REPORT\n")
        f.write("==================================================\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {total_txns}\n")
        f.write("==================================================\n\n")
        
        # 2. OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("--------------------------------------------------\n")
        f.write(f"Total Revenue:       ${total_revenue:,.2f}\n")
        f.write(f"Total Transactions:  {total_txns}\n")
        f.write(f"Average Order Value: ${avg_order_val:,.2f}\n")
        f.write(f"Date Range:          {date_range}\n\n")
        
        # 3. REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("--------------------------------------------------\n")
        f.write(f"{'Region':<15} {'Sales':<15} {'% of Total':<15} {'Transactions':<15}\n")
        # Sort by sales amount descending
        sorted_regions = sorted(region_stats.items(), key=lambda x: x[1]['total_sales'], reverse=True)
        for region, stats in sorted_regions:
            f.write(f"{region:<15} ${stats['total_sales']:<14,.2f} {stats['percentage']:<14}% {stats['transaction_count']:<15}\n")
        f.write("\n")
        
        # 4. TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("--------------------------------------------------\n")
        f.write(f"{'Rank':<5} {'Product Name':<30} {'Qty Sold':<10} {'Revenue':<15}\n")
        for i, (name, qty, rev) in enumerate(top_products, 1):
             f.write(f"{i:<5} {name:<30} {qty:<10} ${rev:<15,.2f}\n")
        f.write("\n")
        
        # 5. TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("--------------------------------------------------\n")
        f.write(f"{'Rank':<5} {'Customer ID':<15} {'Total Spent':<15} {'Orders':<10}\n")
        # customer_analysis returns dict, simpler to re-sort list of (id, stats)
        # It's already sorted in the function but returned as dict. 
        # Dicts preserve insertion order in modern python, but let's be safe.
        # WAIT: the function `customer_analysis` returns a dict where keys are IDs.
        # I need to re-sort here or trust insertion order. Let's re-sort to be safe.
        sorted_cust_list = sorted(customer_stats.items(), key=lambda x: x[1]['total_spent'], reverse=True)[:5]
        for i, (c_id, stats) in enumerate(sorted_cust_list, 1):
            f.write(f"{i:<5} {c_id:<15} ${stats['total_spent']:<14,.2f} {stats['purchase_count']:<10}\n")
        f.write("\n")
        
        # 6. DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("--------------------------------------------------\n")
        f.write(f"{'Date':<15} {'Revenue':<15} {'Txns':<10} {'Unique Cust':<15}\n")
        for date, stats in daily_trends.items():
            f.write(f"{date:<15} ${stats['revenue']:<14,.2f} {stats['transaction_count']:<9} {stats['unique_customers']:<15}\n")
        f.write("\n")
        
        # 7. PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("--------------------------------------------------\n")
        if peak_day[0]:
            f.write(f"Best Selling Day: {peak_day[0]} (Revenue: ${peak_day[1]:,.2f}, Txns: {peak_day[2]})\n")
        else:
            f.write("Best Selling Day: N/A\n")
            
        f.write("Low Performing Products (Qty < 5):\n")
        if low_products:
             for name, qty, rev in low_products:
                 f.write(f"  - {name}: {qty} sold (${rev:,.2f})\n")
        else:
            f.write("  None\n")
        f.write("\n")
            
        # 8. API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("--------------------------------------------------\n")
        f.write(f"Total Products Processed:       {total_enriched}\n")
        f.write(f"Successfully Enriched:          {successful_enrichment}\n")
        f.write(f"Enrichment Success Rate:        {success_rate:.2f}%\n")
        if missing_products:
            f.write("Products not enriched (Sample): " + ", ".join(missing_products[:5]) + ("..." if len(missing_products)>5 else "") + "\n")
        
    print(f"Report generated successfully to: {output_file}")

