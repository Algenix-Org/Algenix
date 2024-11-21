import openai
import requests
from base_agent import BaseAgent

# Shopify API credentials
shopify_api_key = "your_shopify_api_key"
shopify_store_url = "yourshopifystore.myshopify.com"

# OpenAI API key
openai.api_key = "your_openai_api_key"

class EcommerceAgent(BaseAgent):
    def __init__(self, agent_id, **kwargs):
        super().__init__(agent_id, **kwargs)

    def handle_message(self, message):
        user_input = message.get("content", "")
        language = message.get("language", "en")
        return self.process_customer_query(user_input, language)

    def get_order_status(self, order_id):
        url = f"https://{shopify_store_url}/admin/api/2024-01/orders/{order_id}.json"
        headers = {"X-Shopify-Access-Token": shopify_api_key}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["order"]["status"]
        else:
            return "Order not found."

    def generate_response(self, user_input):
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

    def recommend_products(self, user_input):
        products = [
            {"id": 1, "name": "Wireless Headphones", "category": "Electronics"},
            {"id": 2, "name": "Running Shoes", "category": "Sportswear"},
            {"id": 3, "name": "Bluetooth Speaker", "category": "Electronics"}
        ]
        if "headphones" in user_input.lower():
            recommended = [product["name"] for product in products if "headphones" in product["name"].lower()]
        elif "shoes" in user_input.lower():
            recommended = [product["name"] for product in products if "shoes" in product["name"].lower()]
        else:
            recommended = [product["name"] for product in products]

        return f"Here are some products you might like: {', '.join(recommended)}"

    def translate_to_english(self, user_input):
        prompt = f"Translate the following text into English: {user_input}"
        response = openai.Completion.create(
            model="gpt-4",
            prompt=prompt,
            temperature=0.3,
            max_tokens=200
        )
        return response.choices[0].text.strip()

    def process_customer_query(self, user_input, language="en"):
        if language != "en":
            user_input = self.translate_to_english(user_input)

        if "order" in user_input.lower():
            order_id = self.extract_order_id(user_input)
            order_status = self.get_order_status(order_id)
            return f"Your order #{order_id} is currently {order_status}. Need anything else?"

        recommendations = self.recommend_products(user_input)
        return f"{recommendations} Can I help with anything else?"

    def extract_order_id(self, user_input):
        # Example logic for extracting order ID
        return "12345"
