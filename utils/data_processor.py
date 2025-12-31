# ==========================================
# Task 2.1: Sales Summary Calculator
# ==========================================

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions.
    Returns: float (total revenue)
    """
    total = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    return total

def region_wise_sales(transactions):
    """
    Analyzes sales by region.
    Returns: dictionary with region statistics sorted by total_sales desc.
    """
    region_stats = {}
    total_revenue = calculate_total_revenue(transactions)
    
    # 1. Aggregate data
    for t in transactions:
        region = t['Region']
        amount = t['Quantity'] * t['UnitPrice']
        
        if region not in region_stats:
            region_stats[region] = {'total_sales': 0.0, 'transaction_count': 0}
            
        region_stats[region]['total_sales'] += amount
        region_stats[region]['transaction_count'] += 1
        
    # 2. Calculate percentage and format
    final_stats = {}
    for region, data in region_stats.items():
        percentage = (data['total_sales'] / total_revenue) * 100 if total_revenue > 0 else 0
        final_stats[region] = {
            'total_sales': round(data['total_sales'], 2),
            'transaction_count': data['transaction_count'],
            'percentage': round(percentage, 2)
        }
        
    # 3. Sort by total_sales descending
    # Converting to a dict to maintain order (Python 3.7+)
    sorted_stats = dict(sorted(final_stats.items(), key=lambda item: item[1]['total_sales'], reverse=True))
    
    return sorted_stats

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold.
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """
    product_stats = {}
    
    # 1. Aggregate
    for t in transactions:
        p_name = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']
        
        if p_name not in product_stats:
            product_stats[p_name] = {'qty': 0, 'revenue': 0.0}
            
        product_stats[p_name]['qty'] += qty
        product_stats[p_name]['revenue'] += revenue
        
    # 2. Convert to list of tuples
    result_list = [
        (name, stats['qty'], round(stats['revenue'], 2)) 
        for name, stats in product_stats.items()
    ]
    
    # 3. Sort by TotalQuantity descending
    result_list.sort(key=lambda x: x[1], reverse=True)
    
    # 4. Return top n
    return result_list[:n]

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns.
    Returns: dictionary of customer statistics sorted by total_spent desc.
    """
    cust_stats = {}
    
    # 1. Aggregate
    for t in transactions:
        cid = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        p_name = t['ProductName']
        
        if cid not in cust_stats:
            cust_stats[cid] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_set': set() # Using set for uniqueness
            }
            
        cust_stats[cid]['total_spent'] += amount
        cust_stats[cid]['purchase_count'] += 1
        cust_stats[cid]['products_set'].add(p_name)
        
    # 2. Format final output
    final_cust_stats = {}
    for cid, data in cust_stats.items():
        avg_value = data['total_spent'] / data['purchase_count'] if data['purchase_count'] > 0 else 0
        
        final_cust_stats[cid] = {
            'total_spent': round(data['total_spent'], 2),
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(avg_value, 2),
            'products_bought': list(data['products_set']) # Convert set back to list
        }
        
    # 3. Sort by total_spent descending
    sorted_cust = dict(sorted(final_cust_stats.items(), key=lambda item: item[1]['total_spent'], reverse=True))
    
    return sorted_cust


# ==========================================
# Task 2.2: Date-based Analysis
# ==========================================

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date.
    Returns: dictionary sorted by date.
    """
    daily_stats = {}
    
    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']
        cid = t['CustomerID']
        
        if date not in daily_stats:
            daily_stats[date] = {
                'revenue': 0.0, 
                'transaction_count': 0, 
                'customers_set': set()
            }
            
        daily_stats[date]['revenue'] += amount
        daily_stats[date]['transaction_count'] += 1
        daily_stats[date]['customers_set'].add(cid)
        
    # Format and Sort
    final_daily = {}
    # Sorting keys (dates) chronologically
    sorted_dates = sorted(daily_stats.keys())
    
    for date in sorted_dates:
        stats = daily_stats[date]
        final_daily[date] = {
            'revenue': round(stats['revenue'], 2),
            'transaction_count': stats['transaction_count'],
            'unique_customers': len(stats['customers_set'])
        }
        
    return final_daily

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue.
    Returns: tuple (date, revenue, transaction_count)
    """
    trend = daily_sales_trend(transactions)
    
    if not trend:
        return None
        
    # Find max based on revenue
    peak_date = max(trend, key=lambda d: trend[d]['revenue'])
    peak_stats = trend[peak_date]
    
    return (peak_date, peak_stats['revenue'], peak_stats['transaction_count'])


# ==========================================
# Task 2.3: Product Performance
# ==========================================

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales (quantity < threshold).
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue) sorted by Qty asc.
    """
    # Reuse aggregation logic from top_selling_products
    product_stats = {}
    
    for t in transactions:
        p_name = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']
        
        if p_name not in product_stats:
            product_stats[p_name] = {'qty': 0, 'revenue': 0.0}
            
        product_stats[p_name]['qty'] += qty
        product_stats[p_name]['revenue'] += revenue
        
    # Filter by threshold
    low_performers = [
        (name, stats['qty'], round(stats['revenue'], 2))
        for name, stats in product_stats.items()
        if stats['qty'] < threshold
    ]
    
    # Sort by TotalQuantity ascending (Low to High)
    low_performers.sort(key=lambda x: x[1])
    
    return low_performers

from utils.file_handler import save_enriched_data

# ==========================================
# Task 3.2: Enrich Sales Data
# ==========================================

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information and saves to file.
    """
    enriched_list = []
    
    for txn in transactions:
        # Create a copy to avoid modifying original list in place if not intended
        enriched_txn = txn.copy()
        
        # 1. Extract Numeric ID (P101 -> 101)
        try:
            p_id_str = txn['ProductID']
            # Remove 'P' and convert to int. Handle cases where format might be off.
            if p_id_str.startswith('P'):
                numeric_id = int(p_id_str[1:]) 
            else:
                numeric_id = int(p_id_str)
        except ValueError:
            numeric_id = -1 # Invalid ID format
            
        # 2. Lookup in Mapping
        if numeric_id in product_mapping:
            info = product_mapping[numeric_id]
            enriched_txn['API_Category'] = info['category']
            enriched_txn['API_Brand'] = info['brand']
            enriched_txn['API_Rating'] = info['rating']
            enriched_txn['API_Match'] = True
        else:
            enriched_txn['API_Category'] = None
            enriched_txn['API_Brand'] = None
            enriched_txn['API_Rating'] = None
            enriched_txn['API_Match'] = False
            
        enriched_list.append(enriched_txn)
        
    # 3. Save to file (Calling the helper function from file_handler)
    save_enriched_data(enriched_list)
    
    return enriched_list 