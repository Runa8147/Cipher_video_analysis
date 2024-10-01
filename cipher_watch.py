import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configure the Gemini API
genai.configure(api_key='AIzaSyDKv4gjBMYe_OszgWMz7Lcns4900oVBhP0')
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get Gemini response for image analysis
def analyze_image(image):
    prompt = "analyze the image and detect objects and list out the objects. Nothing else in the response. You are an object detection tool."
    response = model.generate_content([image, prompt])
    return response.text

# Streamlit app configuration
st.title("Gemini Image Analysis Tool")

# Sidebar options for choosing between camera or file upload
st.sidebar.title("Choose Image Input Method")
input_method = st.sidebar.radio("Select input method", ("Upload from file", "Capture from camera"))

image = None

# File upload option
if input_method == "Upload from file":
    uploaded_file = st.sidebar.file_uploader("Upload an image (JPG, PNG, or SVG):", type=["jpg", "jpeg", "png", "svg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

# Camera capture option
elif input_method == "Capture from camera":
    img_file_buffer = st.sidebar.camera_input("Take a picture")
    if img_file_buffer:
        bytes_data = img_file_buffer.getvalue()
        image = Image.open(io.BytesIO(bytes_data))
        st.image(image, caption="Captured Image", use_column_width=True)

# Analyze image button
if image is not None:
    if st.button("Analyze Image"):
        response = analyze_image(image)
        st.subheader("AI Analysis:")
        st.write(response)
else:
    st.error("Please upload an image or take a picture.")
