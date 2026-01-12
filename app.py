# #python app.py



from flask import Flask, render_template, request
import requests

app = Flask(__name__)

RAPIDAPI_KEY = "070feea429msh919545bfc7a9170p14c8f4jsn754f6e51c9b0"
RAPIDAPI_HOST = "real-time-amazon-data.p.rapidapi.com"

def get_products(query):
    """Fetch Amazon products or fallback to sample data"""
    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    params = {"query": query, "country": "US", "page": "1"}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        print("API Response:", data)
        
        products = []
        for item in data.get("data", {}).get("products", []):
            # PRODUCT FILTERING - Yeh naya code add karo
            product_name = item.get("product_title", "").lower()
            query_lower = query.lower()
            
            # Check if product actually matches the search query
            is_relevant = (
                query_lower in product_name or 
                any(word in product_name for word in query_lower.split()) or
                len(query_lower) <= 3  # Short queries ke liye strict checking nahi
            )
            
            if not is_relevant:
                continue  # Skip unrelated products
                
            rating = item.get("product_star_rating", "0")
            reviews = item.get("product_num_ratings", "0")
            
            products.append({
                "name": item.get("product_title", "No Title"),
                "price": item.get("product_price", "N/A"),
                "image_url": item.get("product_photo", "/static/default_product.png"),
                "rating": float(rating) if rating else 0,
                "reviews": reviews,
                "url": item.get("product_url", "#")
            })

        # Agar filtered products kam hain toh sample add karo
        if len(products) < 4:
            products.extend(get_sample_products(query))
            
        products = sorted(products, key=lambda x: x["rating"], reverse=True)
        return products[:12]

    except Exception as e:
        print("API error:", e)
        return get_sample_products(query)

def get_sample_products(query):
    """Sample products for fallback"""
    sample_iphones = [
        {
            "name": f"Apple iPhone {query} Pro Max",
            "price": "$1199",
            "image_url": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-pro-finish-select-202309-6-7inch-naturaltitanium?wid=600&hei=600&fmt=jpeg",
            "rating": 4.8,
            "reviews": "45,000",
            "url": "https://www.apple.com/iphone-15-pro/"
        },
        {
            "name": f"Apple iPhone {query} Pro",
            "price": "$999",
            "image_url": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-pro-finish-select-202309-6-7inch-bluetitanium?wid=600&hei=600&fmt=jpeg",
            "rating": 4.7,
            "reviews": "38,000",
            "url": "https://www.apple.com/iphone-15-pro/"
        },
        {
            "name": f"Apple iPhone {query}",
            "price": "$799",
            "image_url": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-finish-select-202309-6-1inch-pink?wid=600&hei=600&fmt=jpeg",
            "rating": 4.6,
            "reviews": "32,000",
            "url": "https://www.apple.com/iphone-15/"
        }
    ]
    
    sample_laptops = [
        {
            "name": f"MacBook Pro {query}",
            "price": "$1299",
            "image_url": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp-14-spacegray-select-202301?wid=600&hei=600&fmt=jpeg",
            "rating": 4.8,
            "reviews": "12,000",
            "url": "https://www.apple.com/macbook-pro/"
        }
    ]
    
    if "iphone" in query.lower():
        return sample_iphones
    elif "laptop" in query.lower() or "macbook" in query.lower():
        return sample_laptops
    else:
        return sample_iphones  # Default

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    products = []

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            products = get_products(query)

    return render_template("main.html", products=products, query=query)

@app.route("/test")
def test():
    return "✅ Flask is working!"

if __name__ == "__main__":
    print("🚀 Starting AI Product Search Engine...")
    print("📍 http://localhost:5000")
    app.run(debug=True, port=5000)