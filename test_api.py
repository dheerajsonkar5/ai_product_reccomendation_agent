import requests
import json

# Your API credentials
RAPIDAPI_KEY = "070feea429msh919545bfc7a9170p14c8f4jsn754f6e51c9b0"
RAPIDAPI_HOST = "real-time-amazon-data.p.rapidapi.com"

def test_api():
    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    
    params = {
        "query": "laptop",
        "page": "1",
        "country": "US"
    }
    

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    try:
        print("🔍 Testing API connection...")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📦 Response Headers: {dict(response.headers)}")
        
        data = response.json()
        print(f"🎯 Full Response: {json.dumps(data, indent=2)}")
        
        # Check if we have products
        if 'data' in data and 'products' in data['data']:
            products_count = len(data['data']['products'])
            print(f"✅ Found {products_count} products")
            
            if products_count > 0:
                for i, product in enumerate(data['data']['products'][:3]):
                    print(f"📱 Product {i+1}:")
                    print(f"   Name: {product.get('product_title', 'No title')}")
                    print(f"   Price: {product.get('product_price', 'No price')}")
                    print(f"   Rating: {product.get('product_star_rating', 'No rating')}")
                    print("   ---")
        else:
            print("❌ No products found in response")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()