from gradio_client import Client, handle_file

# Initialize the Hugging Face Gradio client with your API token
client = Client("Nymbo/Virtual-Try-On", hf_token='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')

def virtual_try_on(person_image_path, garment_image_path):
    """
    Function to perform virtual try-on using the Gradio client.

    Parameters:
    person_image_path (str): Path to the image of the person.
    garment_image_path (str): Path to the image of the garment.

    Returns:
    str: The result image path.
    """
    try:
        # Call the predict function
        result = client.predict(
            {"background": handle_file(person_image_path), "layers": [], "composite": None},  # Input person image
            handle_file(garment_image_path),  # Input garment image
            "Virtual Try On!!",  # Garment description or other input
            is_checked=True,  # Boolean flag for any specific check
            is_checked_crop=False,  # Boolean flag for cropping
            denoise_steps=30,  # Number of denoising steps
            seed=42,  # Seed for reproducibility
            api_name="/tryon"  # Ensure this matches the correct API endpoint
        )

        # Return the result (image path)
        return result[0]
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
#person_image_path = r"images\person_img.jpg"
#garment_image_path = r"images\garment1.jpg"

#result_image_data = virtual_try_on(person_image_path, garment_image_path)

# If the result is not None, display the image
#if result_image_data:
#    image = Image.open(result_image_data)
#    image.show()
