import requests
import openai


# Shopify API credentials (example)
shopify_api_key = "your_shopify_api_key"
shopify_store_url = "yourshopifystore.myshopify.com"

## Openai API

openai.api_key = ""

def get_order_status(order_id):
    url = f"https://{shopify_store_url}/admin/api/2024-01/orders/{order_id}.json"
    headers = {
        "X-Shopify-Access-Token": shopify_api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["order"]["status"]
    else:
        return "Order not found."

# Order tracking feature integrated with the OpenAI chatbot
def handle_customer_query(user_input):
    # Check if user query contains order number (basic validation for demo)
    if "order" in user_input.lower():
        order_id = extract_order_id(user_input)  # Function to extract order ID from the query
        order_status = get_order_status(order_id)
        return f"Your order #{order_id} is currently {order_status}."
    else:
        return generate_response(user_input)

def generate_response(user_input):
    # Use OpenAI to generate general responses
    prompt = f"""
    You are an AI assistant for an e-commerce website. Respond to the customer query based on available knowledge.
    
    Customer Query: "{user_input}"
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful e-commerce customer support assistant."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error: {e}"

def extract_order_id(user_input):
    # Logic to extract order ID (could use regex or keyword-based extraction)
    return "12345"

def recommend_products(user_input):
    # A simple recommendation engine: You can integrate your product catalog here
    products = [
        {"id": 1, "name": "Wireless Headphones", "category": "Electronics"},
        {"id": 2, "name": "Running Shoes", "category": "Sportswear"},
        {"id": 3, "name": "Bluetooth Speaker", "category": "Electronics"}
    ]
    
    # Example: Recommend products based on a keyword in the query
    if "headphones" in user_input.lower():
        recommended = [product["name"] for product in products if "headphones" in product["name"].lower()]
    elif "shoes" in user_input.lower():
        recommended = [product["name"] for product in products if "shoes" in product["name"].lower()]
    else:
        recommended = [product["name"] for product in products]

    return f"Here are some products you might like: {', '.join(recommended)}"

def generate_response(user_input):
    # Combine the order status and product recommendations
    if "order" in user_input.lower():
        order_id = extract_order_id(user_input)
        order_status = get_order_status(order_id)
        return f"Your order #{order_id} is currently {order_status}. Need anything else?"
    
    recommendations = recommend_products(user_input)
    return f"{recommendations} Can I help with anything else?"

def translate_to_english(user_input):
    # Use OpenAI's language model to translate text (or integrate a translation API)
    prompt = f"Translate the following text into English: {user_input}"
    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        temperature=0.3,
        max_tokens=200
    )
    return response.choices[0].text.strip()

def handle_customer_query(user_input, language="en"):
    if language != "en":
        user_input = translate_to_english(user_input)
    return generate_response(user_input)
