import streamlit as st
from twilio.twiml.messaging_response import MessagingResponse
import logging
from urllib.parse import parse_qs
import requests

# Set up logging to a specific file location
logging.basicConfig(
    level=logging.INFO,
    filename='app/logfile.log',  # Set your log file location here
    filemode='a',  # Append mode, use 'w' for overwrite mode
    format='%(asctime)s - %(levelname)s - %(message)s'  # Optional: set the log message format
)

# Streamlit UI
st.title("Virtual Try-On Chatbot")
st.write("Listening for incoming WhatsApp messages from Twilio...")

# A placeholder for displaying messages
message_display = st.empty()

# A placeholder for displaying images
image_display = st.empty()

# Function to handle incoming webhook requests
def handle_webhook():
    # Parse the incoming query params (simulate Twilio webhook)
    params = st.experimental_get_query_params()
    method = params.get("method", [None])[0]
    body = params.get("body", [""])[0]
    
    if method == "POST" and body:
        # Parse the POST body (assuming x-www-form-urlencoded format)
        data = parse_qs(body)

        # Log message details
        message_display.write(f"Message {data}")

        # Extract relevant information from the parsed data
        message_body = data.get('Body', [''])[0].strip()
        from_number = data.get('From', [''])[0]
        media_url = data.get('MediaUrl0', [None])[0]

        # Log message details
        logging.info(f"Message from: {from_number}, Message body: {message_body}")
        if media_url:
            logging.info(f"Received image URL: {media_url}")

        # Update the Streamlit app dynamically with the message
        message_display.write(f"Message from {from_number}: {message_body}")
        if media_url:
            image_display.image(media_url, caption="Received Image")

        # Prepare a Twilio response message (optional)
        response = MessagingResponse()
        if media_url:
            response.message("Image received! Processing now...")
        else:
            response.message("Please send an image to try on!")
        
        # Log the response for debugging
        logging.info(f"Response: {response}")

# Call the webhook handler function
handle_webhook()

