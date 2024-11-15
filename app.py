from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os

# Initialize Flask app
app = Flask(__name__)

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=" + GEMINI_API_KEY  

# Function to determine if a message is finance-related
def is_finance_related(message):
    finance_keywords = ["budget", "expense", "spend", "savings", "income", "investment", "debt", "loan", "finance", "money"]
    return any(keyword in message.lower() for keyword in finance_keywords)

# Function to query the Gemini API
def query_gemini_api(message):
    try:
        response = requests.post(
            GEMINI_API_URL,
            headers={"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"},
            json={"prompt": message, "max_tokens": 100}  # Adjust parameters as needed
        )
        response_data = response.json()
        return response_data.get("response", "Sorry, I couldn't understand that.")
    except Exception as e:
        print(f"Error querying Gemini API: {e}")
        return "Sorry, I'm having trouble processing your request."

# Define the route for incoming WhatsApp messages
@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    print("reached here")
    incoming_msg = request.values.get("Body", "").strip()

    # Log the incoming message
    app.logger.debug(f"Received message: {incoming_msg}")

    if is_finance_related(incoming_msg):
        # Send the finance-related message to Gemini
        bot_reply = query_gemini_api(incoming_msg)
    else:
        bot_reply = "I'm here to assist with finance and budgeting questions only."

    # Create Twilio response
    twilio_response = MessagingResponse()
    twilio_response.message(bot_reply)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(debug=True, port = 5001)
