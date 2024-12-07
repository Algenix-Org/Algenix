# Shopify-OpenAI Integration Documentation

## Overview
This project integrates Shopify's API with OpenAI's GPT-4 to provide a customer support chatbot capable of handling queries related to order statuses, product recommendations, and general customer inquiries. The chatbot supports basic multilingual functionality through translation and can assist with personalized responses.

---

## Features
1. **Order Status Tracking**
   - Retrieves the status of customer orders using Shopify API.
2. **AI-Powered Customer Support**
   - Uses OpenAI’s GPT-4 model to answer customer queries.
3. **Product Recommendations**
   - Recommends products based on keywords in the user's query.
4. **Multilingual Support**
   - Translates customer input to English before processing.

---

## Setup Instructions

### Prerequisites
- Python 3.7+
- Installed `requests` library: `pip install requests`
- OpenAI Python SDK: `pip install openai`

### Configuration
1. **Shopify API Credentials**:
   - Replace `your_shopify_api_key` with your actual Shopify API key.
   - Replace `yourshopifystore.myshopify.com` with your Shopify store URL.

2. **OpenAI API Key**:
   - Replace `openai.api_key` with your OpenAI API key.

---

## Code Components

### 1. Shopify API Integration

#### Function: `get_order_status(order_id)`
Retrieves the status of an order from Shopify using its order ID.

```python
url = f"https://{shopify_store_url}/admin/api/2024-01/orders/{order_id}.json"
headers = {"X-Shopify-Access-Token": shopify_api_key}
response = requests.get(url, headers=headers)
```
- **Parameters**: `order_id` (str)
- **Returns**: Order status (str) or "Order not found."

---

### 2. OpenAI Chatbot Integration

#### Function: `generate_response(user_input)`
Generates an AI-driven response for customer queries.

```python
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful e-commerce customer support assistant."},
        {"role": "user", "content": user_input}
    ],
    temperature=0.7,
    max_tokens=200
)
```
- **Parameters**: `user_input` (str)
- **Returns**: Generated response (str)

#### Function: `translate_to_english(user_input)`
Translates non-English queries into English for processing.

```python
prompt = f"Translate the following text into English: {user_input}"
response = openai.Completion.create(
    model="gpt-4",
    prompt=prompt,
    temperature=0.3,
    max_tokens=200
)
```
- **Parameters**: `user_input` (str)
- **Returns**: Translated text (str)

---

### 3. Customer Query Handling

#### Function: `handle_customer_query(user_input, language="en")`
Processes customer queries and provides responses for both order tracking and product recommendations.

- **Order Queries**: Uses `get_order_status()`.
- **General Queries**: Provides recommendations through `recommend_products()`.

Example:
```python
if "order" in user_input.lower():
    order_id = extract_order_id(user_input)
    order_status = get_order_status(order_id)
    return f"Your order #{order_id} is currently {order_status}. Need anything else?"
```

#### Function: `recommend_products(user_input)`
Recommends products based on keywords in the query.

- **Example Keywords**: "headphones," "shoes."
- **Response**: List of matching products.

```python
products = [
    {"id": 1, "name": "Wireless Headphones", "category": "Electronics"},
    {"id": 2, "name": "Running Shoes", "category": "Sportswear"},
    {"id": 3, "name": "Bluetooth Speaker", "category": "Electronics"}
]
```

---

## Usage Example

### Sample Query: Order Status
**Input**:
> "What is the status of my order #12345?"

**Response**:
> "Your order #12345 is currently shipped."

### Sample Query: Product Recommendation
**Input**:
> "Do you have any headphones?"

**Response**:
> "Here are some products you might like: Wireless Headphones. Can I help with anything else?"

---

## Enhancements
- **Order ID Extraction**: Improve `extract_order_id` to use regular expressions for better accuracy.
- **Product Catalog**: Connect to a dynamic product database for recommendations.
- **Translation API**: Use a dedicated translation service for better multilingual support.

---

## Known Limitations
1. **Static Data**: Product recommendations are hardcoded.
2. **Error Handling**: Limited error messages for API failures.
3. **Order ID Extraction**: Basic extraction logic.

---

## Conclusion
This project demonstrates a functional integration of Shopify's API and OpenAI’s GPT-4 to create a chatbot capable of managing e-commerce customer interactions. With further refinements, it can become a comprehensive solution for automated customer support.

