import sys
import time

# Import our custom modules
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue, region_wise_sales, top_selling_products, 
    customer_analysis, daily_sales_trend, enrich_sales_data
)
from utils.api_handler import fetch_all_products, create_product_mapping
from utils.report_generator import generate_sales_report

def main():
    """
    Main execution function for the Sales Analytics System.
    """
    print("=" * 40)
    print("SALES ANALYTICS SYSTEM")
    print("=" * 40)
    print("")

    try:
        # ---------------------------------------------------------
        # 1 & 2. Read Sales Data
        # ---------------------------------------------------------
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data('data/sales_data.txt')
        
        if not raw_lines:
            print("Error: No data found. Exiting.")
            return

        print(f"✓ Successfully read {len(raw_lines)} transactions")
        print("")

        # ---------------------------------------------------------
        # 3. Parse and Clean
        # ---------------------------------------------------------
        print("[2/10] Parsing and cleaning data...")
        parsed_transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed_transactions)} records")
        print("")

        # ---------------------------------------------------------
        # 4. Display Filter Options
        # ---------------------------------------------------------
        print("[3/10] Filter Options Available:")
        
        # Calculate available options dynamically for display
        if parsed_transactions:
            regions = sorted(list(set(t['Region'] for t in parsed_transactions)))
            amounts = [t['Quantity'] * t['UnitPrice'] for t in parsed_transactions]
            min_amt = min(amounts) if amounts else 0
            max_amt = max(amounts) if amounts else 0
            
            print(f"Regions: {', '.join(regions)}")
            print(f"Amount Range: ₹{min_amt:,.0f} - ₹{max_amt:,.0f}")
        
        print("")
        user_filter = input("Do you want to filter data? (y/n): ").strip().lower()
        print("")

        # ---------------------------------------------------------
        # 5. Get Filter Criteria (if 'y')
        # ---------------------------------------------------------
        filter_region = None
        filter_min = None
        filter_max = None

        if user_filter == 'y':
            print("--- Enter Filter Criteria (Press Enter to skip) ---")
            
            # Get Region
            r_input = input("Enter Region: ").strip()
            if r_input:
                filter_region = r_input
            
            # Get Min Amount
            min_input = input("Min Amount: ").strip()
            if min_input:
                try:
                    filter_min = float(min_input)
                except ValueError:
                    print("Invalid number for Min Amount. Ignoring.")

            # Get Max Amount
            max_input = input("Max Amount: ").strip()
            if max_input:
                try:
                    filter_max = float(max_input)
                except ValueError:
                    print("Invalid number for Max Amount. Ignoring.")
            print("")

        # ---------------------------------------------------------
        # 6 & 7. Validate and Apply Filters
        # ---------------------------------------------------------
        print("[4/10] Validating transactions...")
        
        # This function handles both validation AND filtering logic
        valid_transactions, invalid_count, summary = validate_and_filter(
            parsed_transactions, 
            region=filter_region, 
            min_amount=filter_min, 
            max_amount=filter_max
        )
        
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")
        
        if not valid_transactions:
            print("Warning: No valid transactions left after filtering/validation.")
            # We continue, but analysis might be empty
        print("")

        # ---------------------------------------------------------
        # 8. Perform Analyses
        # ---------------------------------------------------------
        print("[5/10] Analyzing sales data...")
        # We call the functions to ensure they run as per requirements
        # (The results are re-calculated in the report generator, but we run them here to validate logic)
        _ = calculate_total_revenue(valid_transactions)
        _ = region_wise_sales(valid_transactions)
        _ = top_selling_products(valid_transactions)
        _ = customer_analysis(valid_transactions)
        _ = daily_sales_trend(valid_transactions)
        
        print("✓ Analysis complete")
        print("")

        # ---------------------------------------------------------
        # 9. Fetch API Data
        # ---------------------------------------------------------
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        
        if not api_products:
            print("Warning: API fetch failed. Enrichment will be skipped.")
        else:
            print(f"✓ Fetched {len(api_products)} products")
        print("")

        # ---------------------------------------------------------
        # 10. Enrich Data
        # ---------------------------------------------------------
        print("[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        
        # Calculate stats for display
        enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
        total_count = len(enriched_transactions)
        percentage = (enriched_count / total_count * 100) if total_count > 0 else 0
        
        print(f"✓ Enriched {enriched_count}/{total_count} transactions ({percentage:.1f}%)")
        print("")

        # ---------------------------------------------------------
        # 11. Save Enriched Data
        # ---------------------------------------------------------
        print("[8/10] Saving enriched data...")
        # Note: enrich_sales_data() already called the save function internally 
        # as per Task 3.2 requirements. We just confirm the location here.
        print("✓ Saved to: data/enriched_sales_data.txt")
        print("")

        # ---------------------------------------------------------
        # 12. Generate Report
        # ---------------------------------------------------------
        print("[9/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions, 'output/sales_report.txt')
        print("✓ Report saved to: output/sales_report.txt")
        print("")

        # ---------------------------------------------------------
        # 13. Final Success Message
        # ---------------------------------------------------------
        print("[10/10] Process Complete!")
        print("========================================")

    except Exception as e:
        print("\n!!! CRITICAL SYSTEM ERROR !!!")
        print(f"An unexpected error occurred: {e}")
        print("Please check your data files and try again.")
        print("========================================")

if __name__ == "__main__":
    main()