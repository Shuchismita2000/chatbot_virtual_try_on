import streamlit as st
from gradio_client import Client, handle_file
import requests
import httpx
import asyncio

# Title of the app
st.title("Virtual Try-On App")

# Introduction
st.write("Upload your image and an image of the garment you'd like to try on!")

# Image uploader for user photo
user_image = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])
garment_image = st.file_uploader("Upload the garment image", type=["jpg", "jpeg", "png"])

# Placeholder for displaying the result
result_display = st.empty()

# Define the function to call the Gradio API
async def call_tryon_api(user_image_data, garment_image_data):
    # Initialize the Gradio client with the space name
    client = Client("Nymbo/Virtual-Try-On")
    
    # Send the API request
    result = client.predict(
        dict={
            "background": handle_file(user_image_data),
            "layers": [],
            "composite": None
        },
        garm_img=handle_file(garment_image_data),
        garment_des="virtual try on",
        is_checked=True,
        is_checked_crop=False,
        denoise_steps=20,
        seed=42,
        api_name="/tryon"
    )
    
    # Extract the result URL
    url = result[0]
    return url

# Button to submit images and call the API
if st.button("Try On"):
    if user_image and garment_image:
        # Display uploaded images
        st.image(user_image, caption="Your Image", use_column_width=True)
        st.image(garment_image, caption="Garment Image", use_column_width=True)

        # Call the API asynchronously
        user_img_data = user_image.read()
        garment_img_data = garment_image.read()
        
        # Use asyncio to call the async function
        async def run_async():
            result_url = await call_tryon_api(user_img_data, garment_img_data)
            result_display.image(result_url, caption="Try-On Result", use_column_width=True)

        asyncio.run(run_async())

    else:
        st.warning("Please upload both your image and a garment image.")


