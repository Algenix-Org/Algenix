import logging
from datetime import datetime

# Simple logging setup for chatbot interactions
logging.basicConfig(filename="chatbot_logs.log", level=logging.INFO)

def log_interaction(user_input, bot_response):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{timestamp} - User: {user_input} | Bot: {bot_response}"
    logging.info(log_message)
