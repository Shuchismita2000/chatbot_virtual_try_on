import streamlit as st
from twilio.twiml.messaging_response import MessagingResponse
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Custom handler for HTTP requests
class TwilioWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the length of the content and the payload
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        logging.info(f"Received POST data: {post_data}")

        # Parse the POST data
        data = {key: value for key, value in (pair.split('=') for pair in post_data.split('&'))}
        message_body = data.get('Body', '').strip()
        from_number = data.get('From', '')
        media_url = data.get('MediaUrl0', None)

        # Log message details
        logging.info(f"Message from: {from_number}, Message body: {message_body}")
        if media_url:
            logging.info(f"Received image URL: {media_url}")

        # Create a Twilio response
        response = MessagingResponse()
        if media_url:
            response.message("Image received! Processing now...")
        else:
            response.message("Please send an image to try on!")

        # Respond back to Twilio
        self.send_response(200)
        self.send_header('Content-type', 'text/xml')
        self.end_headers()
        self.wfile.write(str(response).encode('utf-8'))

# Function to run the server
def run_server():
    server_address = ('', 8502)  # Running on a separate port
    httpd = HTTPServer(server_address, TwilioWebhookHandler)
    logging.info('Starting Twilio webhook server on port 8502...')
    httpd.serve_forever()

# Run the server in a separate thread so it doesn't block the Streamlit app
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Streamlit UI
st.title("Virtual Try-On Chatbot")
st.write("This app listens for Twilio webhook messages at `/webhook` on port 8502.")


