import unittest
from unittest.mock import patch, MagicMock


class TestShopifyBot(unittest.TestCase):

    @patch("shopify_bot.requests.get")
    def test_get_order_status_success(self, mock_get):
        # Mock a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"order": {"status": "shipped"}}
        mock_get.return_value = mock_response

        shopify_store_url = "test-shop.myshopify.com"
        shopify_api_key = "test-api-key"
        
        result = get_order_status(order_id="12345")
        self.assertEqual(result, "shipped")
        mock_get.assert_called_once()

    @patch("shopify_bot.requests.get")
    def test_get_order_status_not_found(self, mock_get):
        # Mock a 404 response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = get_order_status(order_id="12345")
        self.assertEqual(result, "Order not found.")
        mock_get.assert_called_once()

    def test_recommend_products_with_keyword(self):
        user_input = "Can you recommend some headphones?"
        result = recommend_products(user_input)
        self.assertIn("Wireless Headphones", result)
        self.assertNotIn("Running Shoes", result)

    def test_recommend_products_general(self):
        user_input = "Show me all products."
        result = recommend_products(user_input)
        self.assertIn("Wireless Headphones", result)
        self.assertIn("Running Shoes", result)

    @patch("shopify_bot.openai.ChatCompletion.create")
    def test_generate_response_order_query(self, mock_openai):
        # Mock OpenAI response for order-related queries
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message={"content": "Your order #12345 is currently processing."})]
        mock_openai.return_value = mock_response

        result = handle_customer_query("Where is my order?")
        self.assertIn("Your order #12345 is currently", result)

    @patch("shopify_bot.openai.Completion.create")
    def test_translate_to_english(self, mock_openai):
        # Mock OpenAI translation response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text="This is a test.")]
        mock_openai.return_value = mock_response

        result = translate_to_english("Ceci est un test.")
        self.assertEqual(result, "This is a test.")
        mock_openai.assert_called_once()

    @patch("shopify_bot.get_order_status")
    def test_handle_customer_query_order(self, mock_get_order_status):
        mock_get_order_status.return_value = "delivered"
        result = handle_customer_query("What is the status of my order #12345?")
        self.assertIn("Your order #12345 is currently delivered.", result)

    def test_handle_customer_query_recommendations(self):
        result = handle_customer_query("Can you suggest some electronics?")
        self.assertIn("Here are some products you might like", result)
        self.assertIn("Wireless Headphones", result)

if __name__ == "__main__":
    unittest.main()
