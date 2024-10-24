from flask import Flask
from webhook_handler import whatsapp_webhook

app = Flask(__name__)

# Set up the route for the webhook
@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp_webhook_route():
    return whatsapp_webhook()

if __name__ == "__main__":
    app.run(port=5000)
