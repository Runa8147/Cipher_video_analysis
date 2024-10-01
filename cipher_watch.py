import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configure the Gemini API
genai.configure(api_key='api key')
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get Gemini response for image analysis
def analyze_image(image):
    prompt="analyze the image and detect objects and list out the objects.nothing else in the response.you are a object detection tool"
    response = model.generate_content([image,prompt])
    return response.text

# Streamlit app configuration
st.title("Gemini Image Analysis Tool")

# Upload image or capture from camera
uploaded_file = st.file_uploader("Upload an image (JPG, PNG, or SVG):", type=["jpg", "jpeg", "png", "svg"])
img_file_buffer = st.camera_input("Take a picture")

# Display and analyze image
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Analyze Image"):
        response = analyze_image(image)
        st.subheader("AI Analysis:")
        st.write(response)
elif img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    image = Image.open(io.BytesIO(bytes_data))
    st.image(image, caption="Captured Image", use_column_width=True)

    if st.button("Analyze Image"):
        response = analyze_image(image)
        st.subheader("AI Analysis:")
        st.write(response)
else:
    st.error("Please upload an image or take a picture.")
