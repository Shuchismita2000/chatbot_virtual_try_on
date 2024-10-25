
import os
from flask import Flask
from webhook_handler import whatsapp_webhook

app = Flask(__name__)

# Set up the route for the webhook
@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp_webhook_route():
    return whatsapp_webhook()

#if __name__ == '__main__': 
    #port = int(os.environ.get('PORT', 5000)) 
    #app.run(host='0.0.0.0', port=port)
