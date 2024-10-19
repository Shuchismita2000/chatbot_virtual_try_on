import streamlit as st
from twilio.twiml.messaging_response import MessagingResponse
import json
import logging
from urllib.parse import parse_qs

# Set up logging
logging.basicConfig(level=logging.INFO)

# Streamlit's built-in function to show content on the page
st.title("Virtual Try-On Chatbot")
st.write("Webhook status: Listening for incoming messages...")

# Define a webhook handler using Streamlit's built-in support
def handle_webhook():
    if st.experimental_get_query_params().get("method", [None])[0] == "POST":
        # Parse the incoming request body (it's available via st.experimental_get_query_params)
        request_body = st.experimental_get_query_params().get("body", [""])[0]
        data = parse_qs(request_body)

        message_body = data.get('Body', [''])[0].strip()
        from_number = data.get('From', [''])[0]
        media_url = data.get('MediaUrl0', [None])[0]

        # Log the extracted details
        logging.info(f"Message from: {from_number}, Message body: {message_body}")
        if media_url:
            logging.info(f"Received image URL: {media_url}")
            st.write(f"Received image URL: {media_url}")

        # Respond with a simple message (note: this is just for debugging and viewing in logs)
        response = MessagingResponse()
        if media_url:
            response.message("Image received! Processing now...")
        else:
            response.message("Please send an image to try on!")

        # Display response message in Streamlit for verification
        st.write(f"Response: {response}")

# Call the handler function
handle_webhook()


