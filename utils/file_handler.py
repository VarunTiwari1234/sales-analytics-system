import os

# ==========================================
# Task 1.1: Read Sales Data with Encoding Handling
# ==========================================
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    Returns: list of raw lines (strings) without headers or empty lines.
    """
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings_to_try:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                raw_lines = f.readlines()
                
            # If read is successful, process the lines immediately
            clean_lines = []
            for line in raw_lines:
                line = line.strip()
                # Skip empty lines
                if not line:
                    continue
                # Skip header row
                if line.startswith('TransactionID'):
                    continue
                clean_lines.append(line)
            
            return clean_lines

        except UnicodeDecodeError:
            # If this encoding fails, the loop continues to the next one
            continue
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
            return []
            
    # If all encodings fail
    print(f"Error: Could not read '{filename}' with any of the supported encodings.")
    return []

# ==========================================
# Task 1.2: Parse and Clean Data
# ==========================================
def parse_transactions(raw_lines):
    """
    Parses raw lines into a clean list of dictionaries.
    Handles data quality issues like commas in names/numbers.
    """
    parsed_transactions = []
    
    for line in raw_lines:
        parts = line.split('|')
        
        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue
            
        # Unpack fields
        tid, date, pid, pname, qty_str, price_str, cid, region = parts
        
        try:
            # Handle commas in ProductName (remove them)
            clean_pname = pname.replace(',', '').strip()
            
            # Handle commas in numeric fields
            clean_qty = qty_str.replace(',', '')
            clean_price = price_str.replace(',', '')
            
            # Convert to proper types
            quantity = int(clean_qty)
            unit_price = float(clean_price)
            
            # Create dictionary
            record = {
                'TransactionID': tid.strip(),
                'Date': date.strip(),
                'ProductID': pid.strip(),
                'ProductName': clean_pname,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': cid.strip(),
                'Region': region.strip()
            }
            parsed_transactions.append(record)
            
        except ValueError:
            # Skip row if type conversion fails
            continue
            
    return parsed_transactions

# ==========================================
# Task 1.3: Data Validation and Filtering
# ==========================================
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    Returns: tuple (valid_transactions, invalid_count, filter_summary)
    """
    valid_data = []
    invalid_count = 0
    
    # --- Step 1: Validation ---
    for txn in transactions:
        is_valid = True
        
        # Quantity and UnitPrice must be > 0
        if txn['Quantity'] <= 0 or txn['UnitPrice'] <= 0:
            is_valid = False
            
        # ID Format Validation
        if not txn['TransactionID'].startswith('T'):
            is_valid = False
        if not txn['ProductID'].startswith('P'):
            is_valid = False
        if not txn['CustomerID'].startswith('C'):
            is_valid = False
            
        if is_valid:
            valid_data.append(txn)
        else:
            invalid_count += 1

    # --- Step 2: Display Options to User ---
    # Get unique regions for display
    available_regions = sorted(list(set(t['Region'] for t in valid_data)))
    print(f"\n[Info] Available Regions: {available_regions}")
    
    if valid_data:
        amounts = [t['Quantity'] * t['UnitPrice'] for t in valid_data]
        print(f"[Info] Transaction Amount Range: {min(amounts)} - {max(amounts)}")

    # --- Step 3: Filtering ---
    filtered_data = valid_data
    
    # Filter by Region
    if region:
        initial_count = len(filtered_data)
        filtered_data = [t for t in filtered_data if t['Region'].lower() == region.lower()]
        region_removed_count = initial_count - len(filtered_data)
    else:
        region_removed_count = 0
        
    print(f"[Filter] Records after region filter: {len(filtered_data)}")

    # Filter by Amount (Min/Max)
    count_before_amount = len(filtered_data)
    if min_amount is not None:
        filtered_data = [t for t in filtered_data if (t['Quantity'] * t['UnitPrice']) >= min_amount]
    
    if max_amount is not None:
        filtered_data = [t for t in filtered_data if (t['Quantity'] * t['UnitPrice']) <= max_amount]
        
    amount_removed_count = count_before_amount - len(filtered_data)
    print(f"[Filter] Records after amount filter: {len(filtered_data)}")

    # --- Step 4: Summary ---
    summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': region_removed_count,
        'filtered_by_amount': amount_removed_count,
        'final_count': len(filtered_data)
    }
    
    return filtered_data, invalid_count, summary

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file with new API columns.
    """
    header = [
        "TransactionID", "Date", "ProductID", "ProductName", "Quantity", 
        "UnitPrice", "CustomerID", "Region", "API_Category", "API_Brand", 
        "API_Rating", "API_Match"
    ]
    
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Write Header
            f.write('|'.join(header) + '\n')
            
            # Write Data
            for txn in enriched_transactions:
                row = [
                    str(txn.get('TransactionID', '')),
                    str(txn.get('Date', '')),
                    str(txn.get('ProductID', '')),
                    str(txn.get('ProductName', '')),
                    str(txn.get('Quantity', '')),
                    str(txn.get('UnitPrice', '')),
                    str(txn.get('CustomerID', '')),
                    str(txn.get('Region', '')),
                    str(txn.get('API_Category', '') if txn.get('API_Category') is not None else ''),
                    str(txn.get('API_Brand', '') if txn.get('API_Brand') is not None else ''),
                    str(txn.get('API_Rating', '') if txn.get('API_Rating') is not None else ''),
                    str(txn.get('API_Match', False))
                ]
                f.write('|'.join(row) + '\n')
                
        print(f"[File] Successfully saved enriched data to {filename}")
        
    except Exception as e:
        print(f"[File] Error saving enriched data: {e}")