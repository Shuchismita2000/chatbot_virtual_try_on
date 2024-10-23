from flask import request
from twilio.twiml.messaging_response import MessagingResponse
from tryon_api import virtual_try_on  # Import the virtual_try_on function
from user_manager import * 



def whatsapp_webhook():
    # Get the user's phone number and message
    user_id = request.values.get('From', '')
    incoming_msg = request.values.get('Body', '').lower()
    media_url = request.values.get('MediaUrl0', '')

    # Retrieve or create a user record in the database
    user = get_or_create_user(user_id)
    step = user.current_step

    # Create Twilio response object
    resp = MessagingResponse()
    msg = resp.message()

    # Handle conversation based on the user's state
    if step == "start":
        if "hi" in incoming_msg:
            msg.body("Hi! I can help you with virtual try-on. You can send an image, and I'll guide you through the process.")
            update_user(user, current_step="awaiting_image")
        else:
            msg.body("Please say 'hi' to start.")
    elif step == "awaiting_image":
        if media_url:
            msg.body("Is this a person image or a garment image? Please reply with 'person' or 'garment'.")
            update_user(user, current_step="awaiting_image_type", image_url=media_url)
        else:
            msg.body("Please upload an image.")
    elif step == "awaiting_image_type":
        if incoming_msg == "person":
            update_user(user, person_image_url=user.person_image_url or user.image_url, current_step="awaiting_garment_image")
            msg.body("Got the person image. Now please upload the garment image.")
        elif incoming_msg == "garment":
            update_user(user, garment_image_url=user.garment_image_url or user.image_url, current_step="awaiting_person_image")
            msg.body("Got the garment image. Now please upload the person image.")
        else:
            msg.body("Please reply with either 'person' or 'garment'.")
    elif step == "awaiting_person_image":
        if media_url:
            update_user(user, person_image_url=media_url, current_step="ready_to_try_on")
            msg.body("Got both images! Type 'try on' to proceed.")
        else:
            msg.body("Please upload the person image.")
    elif step == "awaiting_garment_image":
        if media_url:
            update_user(user, garment_image_url=media_url, current_step="ready_to_try_on")
            msg.body("Got both images! Type 'try on' to proceed.")
        else:
            msg.body("Please upload the garment image.")
    elif step == "ready_to_try_on":
        if "try on" in incoming_msg:
            msg.body("Processing your try-on request. Please wait...")
            try:
                # Get the stored images
                person_image = user.person_image_url
                garment_image = user.garment_image_url
                result_image = virtual_try_on(person_image, garment_image)
                msg.media(result_image)  # Respond with the result image
                reset_user(user)  # Reset user state after completion
            except Exception as e:
                msg.body(f"An error occurred: {str(e)}")
        else:
            msg.body("Please type 'try on' to proceed.")
    else:
        msg.body("Something went wrong. Let's start again. Please say 'hi' to restart.")
        reset_user(user)

    return str(resp)
