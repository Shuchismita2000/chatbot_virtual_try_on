import streamlit as st
from PIL import Image
from io import BytesIO
import tempfile

# Import the virtual_try_on function
from gradio_api import virtual_try_on  # Replace 'your_module' with the actual module name

# Title of the app
st.title("Virtual Try-On App")

# Introduction
st.write("Upload your image and an image of the garment you'd like to try on!")

# Image uploader for user photo and garment image
user_image = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])
garment_image = st.file_uploader("Upload the garment image", type=["jpg", "jpeg", "png"])

# Placeholder for displaying the result
result_display = st.empty()

# Button to submit images and call the virtual try-on function
if st.button("Try On"):
    if user_image and garment_image:
        # Display uploaded images
        st.image(user_image, caption="Your Image", use_column_width=True)
        st.image(garment_image, caption="Garment Image", use_column_width=True)

        # Save the uploaded files temporarily and get their file paths
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as user_img_temp, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as garment_img_temp:
            user_img_temp.write(user_image.read())
            garment_img_temp.write(garment_image.read())

            # Call the virtual_try_on function with the temporary file paths
            result_image_data = virtual_try_on(user_img_temp.name, garment_img_temp.name)

        # If the result image is successfully returned
        if result_image_data:
            result_image = Image.open(result_image_data[0])
            result_display.image(result_image, caption="Try-On Result", use_column_width=True)
        else:
            st.error("An error occurred while processing your try-on request.")

    else:
        st.warning("Please upload both your image and a garment image.")
