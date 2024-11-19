import openai

# OpenAI API Key
openai.api_key = "your_openai_api_key"

def handle_customer_query(user_input):
    # Define the context for the chatbot
    prompt = f"""
    You are an AI customer support assistant for an e-commerce website. Respond to the customer's query in a professional and helpful tone.
    
    Customer Query: "{user_input}"
    
    If it's an order-related question, provide a sample tracking response. If it's a product inquiry, suggest relevant products.
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

# Example interaction
customer_query = "Where is my order #12345?"
response = handle_customer_query(customer_query)
print(response)
