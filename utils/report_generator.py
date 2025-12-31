import datetime
import os

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report.
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    report_lines = []
    
    # --- Helper: Currency Formatter ---
    def fmt_currency(amount):
        return f"₹{amount:,.2f}"

    # ==========================================
    # 1. HEADER
    # ==========================================
    gen_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_records = len(transactions)
    
    report_lines.append("=" * 60)
    report_lines.append(f"{'SALES ANALYTICS REPORT':^60}")
    report_lines.append(f"{f'Generated: {gen_date}':^60}")
    report_lines.append(f"{f'Records Processed: {total_records}':^60}")
    report_lines.append("=" * 60)
    report_lines.append("")

    # ==========================================
    # 2. OVERALL SUMMARY
    # ==========================================
    total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    avg_order_value = total_revenue / total_records if total_records > 0 else 0
    
    dates = [t['Date'] for t in transactions]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"
    
    report_lines.append("OVERALL SUMMARY")
    report_lines.append("-" * 60)
    report_lines.append(f"{'Total Revenue:':<25} {fmt_currency(total_revenue)}")
    report_lines.append(f"{'Total Transactions:':<25} {total_records}")
    report_lines.append(f"{'Average Order Value:':<25} {fmt_currency(avg_order_value)}")
    report_lines.append(f"{'Date Range:':<25} {date_range}")
    report_lines.append("")

    # ==========================================
    # 3. REGION-WISE PERFORMANCE
    # ==========================================
    region_stats = {}
    for t in transactions:
        r = t['Region']
        amt = t['Quantity'] * t['UnitPrice']
        if r not in region_stats:
            region_stats[r] = {'sales': 0.0, 'count': 0}
        region_stats[r]['sales'] += amt
        region_stats[r]['count'] += 1
        
    # Sort by sales descending
    sorted_regions = sorted(region_stats.items(), key=lambda x: x[1]['sales'], reverse=True)
    
    report_lines.append("REGION-WISE PERFORMANCE")
    report_lines.append("-" * 60)
    report_lines.append(f"{'Region':<15} {'Sales':<15} {'% of Total':<12} {'Transactions':<12}")
    report_lines.append("-" * 60)
    
    for region, data in sorted_regions:
        pct = (data['sales'] / total_revenue * 100) if total_revenue > 0 else 0
        line = f"{region:<15} {fmt_currency(data['sales']):<15} {pct:>9.2f}% {data['count']:>12}"
        report_lines.append(line)
    report_lines.append("")

    # ==========================================
    # 4. TOP 5 PRODUCTS
    # ==========================================
    prod_stats = {}
    for t in transactions:
        p = t['ProductName']
        if p not in prod_stats:
            prod_stats[p] = {'qty': 0, 'rev': 0.0}
        prod_stats[p]['qty'] += t['Quantity']
        prod_stats[p]['rev'] += t['Quantity'] * t['UnitPrice']
        
    sorted_prods = sorted(prod_stats.items(), key=lambda x: x[1]['qty'], reverse=True)[:5]
    
    report_lines.append("TOP 5 PRODUCTS")
    report_lines.append("-" * 60)
    report_lines.append(f"{'Rank':<6} {'Product Name':<25} {'Qty Sold':<10} {'Revenue':<15}")
    report_lines.append("-" * 60)
    
    for i, (name, data) in enumerate(sorted_prods, 1):
        line = f"{i:<6} {name[:23]:<25} {data['qty']:<10} {fmt_currency(data['rev']):<15}"
        report_lines.append(line)
    report_lines.append("")

    # ==========================================
    # 5. TOP 5 CUSTOMERS
    # ==========================================
    cust_stats = {}
    for t in transactions:
        c = t['CustomerID']
        if c not in cust_stats:
            cust_stats[c] = {'spent': 0.0, 'count': 0}
        cust_stats[c]['spent'] += t['Quantity'] * t['UnitPrice']
        cust_stats[c]['count'] += 1
        
    sorted_cust = sorted(cust_stats.items(), key=lambda x: x[1]['spent'], reverse=True)[:5]
    
    report_lines.append("TOP 5 CUSTOMERS")
    report_lines.append("-" * 60)
    report_lines.append(f"{'Rank':<6} {'Customer ID':<15} {'Total Spent':<15} {'Orders':<10}")
    report_lines.append("-" * 60)
    
    for i, (cid, data) in enumerate(sorted_cust, 1):
        line = f"{i:<6} {cid:<15} {fmt_currency(data['spent']):<15} {data['count']:<10}"
        report_lines.append(line)
    report_lines.append("")

    # ==========================================
    # 6. DAILY SALES TREND
    # ==========================================
    daily_stats = {}
    for t in transactions:
        d = t['Date']
        if d not in daily_stats:
            daily_stats[d] = {'rev': 0.0, 'txns': 0, 'custs': set()}
        daily_stats[d]['rev'] += t['Quantity'] * t['UnitPrice']
        daily_stats[d]['txns'] += 1
        daily_stats[d]['custs'].add(t['CustomerID'])
        
    sorted_days = sorted(daily_stats.keys())
    
    report_lines.append("DAILY SALES TREND")
    report_lines.append("-" * 60)
    report_lines.append(f"{'Date':<15} {'Revenue':<15} {'Txns':<10} {'Unique Cust':<12}")
    report_lines.append("-" * 60)
    
    for d in sorted_days:
        data = daily_stats[d]
        line = f"{d:<15} {fmt_currency(data['rev']):<15} {data['txns']:<10} {len(data['custs']):<12}"
        report_lines.append(line)
    report_lines.append("")

    # ==========================================
    # 7. PRODUCT PERFORMANCE ANALYSIS
    # ==========================================
    # Best selling day
    best_day = max(daily_stats.items(), key=lambda x: x[1]['rev']) if daily_stats else ("N/A", {'rev': 0})
    
    # Low performing products (Quantity < 5 as arbitrary threshold for "low")
    low_perf = [p for p, data in prod_stats.items() if data['qty'] < 5]
    
    report_lines.append("PRODUCT PERFORMANCE ANALYSIS")
    report_lines.append("-" * 60)
    report_lines.append(f"Best Selling Day: {best_day[0]} (Revenue: {fmt_currency(best_day[1]['rev'])})")
    
    low_perf_str = ", ".join(low_perf) if low_perf else "None"
    report_lines.append(f"Low Performing Products (<5 sold): {low_perf_str}")
    
    report_lines.append("Average Transaction Value per Region:")
    for region, data in sorted_regions:
        avg_reg = data['sales'] / data['count'] if data['count'] > 0 else 0
        report_lines.append(f"  - {region}: {fmt_currency(avg_reg)}")
    report_lines.append("")

    # ==========================================
    # 8. API ENRICHMENT SUMMARY
    # ==========================================
    total_enriched = sum(1 for t in enriched_transactions if t.get('API_Match'))
    success_rate = (total_enriched / len(enriched_transactions) * 100) if enriched_transactions else 0
    
    # Find products that failed enrichment (unique names)
    failed_prods = set(t['ProductName'] for t in enriched_transactions if not t.get('API_Match'))
    
    report_lines.append("API ENRICHMENT SUMMARY")
    report_lines.append("-" * 60)
    report_lines.append(f"Total Products Enriched: {total_enriched}")
    report_lines.append(f"Success Rate: {success_rate:.2f}%")
    
    if failed_prods:
        report_lines.append("Products Not Found in API:")
        for p in list(failed_prods)[:5]: # Show max 5 to keep it clean
            report_lines.append(f"  - {p}")
        if len(failed_prods) > 5:
            report_lines.append(f"  ...and {len(failed_prods)-5} more.")
    else:
        report_lines.append("All products successfully enriched!")
        
    report_lines.append("=" * 60)

    # ==========================================
    # WRITE TO FILE
    # ==========================================
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        print(f"[Report] Successfully generated report at: {output_file}")
    except Exception as e:
        print(f"[Report] Error writing report file: {e}")