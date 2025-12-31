pip install requests
import requests

# ==========================================
# Task 3.1: Fetch Product Details
# ==========================================

def fetch_all_products():
    """
    Fetches all products from DummyJSON API.
    Returns: list of product dictionaries.
    """
    url = "https://dummyjson.com/products?limit=100"
    
    try:
        response = requests.get(url, timeout=10)
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"[API] Success: Fetched {len(products)} products.")
            return products
        else:
            print(f"[API] Error: Failed to fetch data. Status Code: {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"[API] Connection Error: {e}")
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info.
    Parameters: api_products (list)
    Returns: dictionary mapping ID (int) -> product info (dict)
    """
    mapping = {}
    
    for product in api_products:
        p_id = product.get('id')
        
        mapping[p_id] = {
            'title': product.get('title'),
            'category': product.get('category'),
            'brand': product.get('brand'),
            'rating': product.get('rating')
        }
        
    return mapping