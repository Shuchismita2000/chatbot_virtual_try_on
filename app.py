import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Title of the app
st.title("Virtual Try-On App")

# Introduction
st.write("Upload your image and an image of the garment you'd like to try on!")

# Image uploader for user photo
user_image = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])
garment_image = st.file_uploader("Upload the garment image", type=["jpg", "jpeg", "png"])

# Placeholder for displaying the result
result_display = st.empty()

# Button to submit images and call the API
if st.button("Try On"):
    if user_image and garment_image:
        # Display uploaded images
        st.image(user_image, caption="Your Image", use_column_width=True)
        st.image(garment_image, caption="Garment Image", use_column_width=True)

        # Send these images to the model
        # Convert the images into a format suitable for the API (files or byte data)
        user_img_data = user_image.read()
        garment_img_data = garment_image.read()

        # Determine file extension (png or jpeg)
        file_extension_user = "png" if user_image.name.endswith(".png") else "jpeg"
        file_extension_garment = "png" if garment_image.name.endswith(".png") else "jpeg"

        # Call the Hugging Face API
        try:
            headers = {"Authorization": "Bearer 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"}  # Replace with valid token
            response = requests.post(
                "https://huggingface.co/spaces/Nymbo/Virtual-Try-On/run",
                headers=headers,
                files={
                    "person_image": (f"user_image.{file_extension_user}", user_img_data, f"image/{file_extension_user}"),
                    "garment_image": (f"garment_image.{file_extension_garment}", garment_img_data, f"image/{file_extension_garment}"),
                }
            )

            # Check if the API call was successful
            if response.status_code == 200:
                # Get the response image
                result_image = Image.open(BytesIO(response.content))
                result_display.image(result_image, caption="Try-On Result", use_column_width=True)
            else:
                st.error("Error with the API call. Please try again later.")
                st.write("Response Status Code:", response.status_code)
                st.write("Response Text:", response.text)

        except Exception as e:
            st.error("An error occurred while contacting the model.")
            st.write(e)
    else:
        st.warning("Please upload both your image and a garment image.")
