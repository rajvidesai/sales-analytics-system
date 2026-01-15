import os
import sys

# Import custom modules
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue, region_wise_sales, top_selling_products,
    customer_analysis, daily_sales_trend, find_peak_sales_day,
    low_performing_products, generate_sales_report
)
from utils.api_handler import (
    fetch_all_products, create_product_mapping,
    enrich_sales_data, save_enriched_data
)

def main():
    print("===================")
    print("SALES ANALYTICS SYSTEM")
    print("===================")
    
    try:
        # Define paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(base_dir, 'data', 'sales_data.txt')
        enriched_file = os.path.join(base_dir, 'data', 'enriched_sales_data.txt')
        report_file = os.path.join(base_dir, 'output', 'sales_report.txt')

        # 1. Read Sales Data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data(data_file)
        if not raw_lines:
            print("No data found or empty file. Exiting.")
            return
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # 2. Parse Data
        print("\n[2/10] Parsing and cleaning data...")
        parsed_data = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed_data)} records")

        # 3. Filter Options (Interactive)
        # To display available options, we run a preliminary validation/pass
        # But `validate_and_filter` does the printing of stats if we call it.
        # Let's call it first with no filters to get the "Available Regions" printout and valid data for user to see stats.
        # The requirement says "Display filter options... Show available regions... Show transaction amount range".
        # My `validate_and_filter` prints these stats.
        
        print("\n[3/10] Filter Options Available:")
        # We'll run it once just to get stats printed (ignoring return values for now, relying on the function's print)
        # Actually effectively we can just proceed to ask user. 
        # But to show the range, we need to inspect the data or rely on `validate_and_filter` to print it.
        # Let's customize the interaction as requested.
        
        # We need valid data to calculate stats for the prompt
        # So let's validate first without filters
        temp_valid, _, temp_summary = validate_and_filter(parsed_data) 
        # validate_and_filter prints [Data Stats]... which meets the "Show available regions" requirement.
        
        filter_choice = input("\nDo you want to filter data? (y/n): ").strip().lower()
        
        region_filter = None
        min_amt = None
        max_amt = None
        
        if filter_choice == 'y':
            r_input = input("Enter Region to filter by (leave empty for all): ").strip()
            if r_input: 
                region_filter = r_input
            
            min_input = input("Enter Min Amount (leave empty for None): ").strip()
            if min_input:
                try:
                    min_amt = float(min_input)
                except ValueError:
                    print("Invalid number, ignoring min amount.")
            
            max_input = input("Enter Max Amount (leave empty for None): ").strip()
            if max_input:
                try:
                    max_amt = float(max_input)
                except ValueError:
                    print("Invalid number, ignoring max amount.")

        # 4. Validate and Filter (Actual)
        print("\n[4/10] Validating transactions...")
        valid_data, invalid_count, summary = validate_and_filter(
            parsed_data, region=region_filter, min_amount=min_amt, max_amount=max_amt
        )
        print(f"✓ Valid: {len(valid_data)} | Invalid: {invalid_count}")
        
        if not valid_data:
            print("No valid data remaining after filtering. Aborting analysis.")
            return

        # 5. Analyze Sales Data
        print("\n[5/10] Analyzing sales data...")
        # We execute them to ensure they work, results will be used in report generation mostly
        # or we could print them here if we wanted debugging, but requirement says "Perform all... (call all functions)"
        # The `generate_sales_report` calls them internally? 
        # The prompt for Task 5.1 says "8. Perform all data analyses (call all functions from Part 2)".
        # And "12. Generate comprehensive report".
        # `generate_sales_report` in my implementation calls them. 
        # I will trust `generate_sales_report` to do the heavy lifting, 
        # OR I can call them explicitly here to satisfy the "Call all functions" requirement strictly.
        # Let's call them explicitly to be safe and verify no errors.
        _ = calculate_total_revenue(valid_data)
        _ = region_wise_sales(valid_data)
        _ = top_selling_products(valid_data)
        _ = customer_analysis(valid_data)
        _ = daily_sales_trend(valid_data)
        _ = find_peak_sales_day(valid_data)
        _ = low_performing_products(valid_data)
        print("✓ Analysis complete")

        # 6. Fetch Product Data
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # 7. Enrich Sales Data
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_data = enrich_sales_data(valid_data, product_mapping)
        
        enriched_count = sum(1 for t in enriched_data if t.get('API_Match'))
        enrich_pct = (enriched_count / len(valid_data) * 100) if valid_data else 0
        print(f"✓ Enriched {enriched_count}/{len(valid_data)} transactions ({enrich_pct:.1f}%)")

        # 8. Save Enriched Data
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_data, enriched_file)
        print(f"✓ Saved to: {os.path.relpath(enriched_file, base_dir)}")

        # 9. Generate Report
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_data, enriched_data, report_file)
        print(f"✓ Report saved to: {os.path.relpath(report_file, base_dir)}")

        # 10. Completion
        print("\n[10/10] Process Complete!")
        print("=========")

    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("The program encountered an unexpected error and had to stop.")

if __name__ == "__main__":
    main()

