import streamlit as st
st.title("Virtual Try-On Chatbot")
st.write("Welcome to the virtual try-on chatbot!")
# Basic file uploader to test Streamlit's upload capability
uploaded_file = st.file_uploader("Upload an image of the person", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
