import os
import tempfile
import streamlit as st
import google.generativeai as genai
import time
from google.api_core import exceptions as google_exceptions

# Configure Gemini API (replace with your actual API key)
GEMINI_API_KEY = "YOUR_API_KEY"  # Placeholder, replace with your actual key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')  # Replace if using a different model

SUPPORTED_EXTENSIONS = [".mp4", ".avi", ".mov", ".mp3", ".wav", ".png", ".jpg", ".jpeg"]


def process_file(file, prompt, max_retries=3, retry_delay=1):
    if file.name.lower().endswith(tuple(SUPPORTED_EXTENSIONS)):
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as temp_file:
            temp_file.write(file.getvalue())
            temp_file_path = temp_file.name

            try:
                for attempt in range(max_retries):
                    try:
                        response = model.generate_content([temp_file_path, prompt])
                        return response.text
                    except google_exceptions.FailedPrecondition as e:
                        if "not in an ACTIVE state" in str(e) and attempt < max_retries - 1:
                            st.warning(f"File not active yet. Retrying in {retry_delay} seconds...")
                            time.sleep(retry_delay)
                        else:
                            raise
            except Exception as e:
                return f"An error occurred: {str(e)}"
            finally:
                os.unlink(temp_file_path)
    else:
        return "Unsupported file format"


def analyze_file(file):
    return process_file(file, "Analyze and summarize the content of this file.")


def chat_with_ai(messages, file):
    return process_file(file, messages)


st.title("Gemini Chatbot for Audio/Video/Image Analysis")

uploaded_file = st.file_uploader("Upload a file", type=[ext[1:] for ext in SUPPORTED_EXTENSIONS])

if uploaded_file:
    st.write("Analyzing file...")
    summary = analyze_file(uploaded_file)
    if summary.startswith("An error occurred:"):
        st.error(summary)
    else:
        st.write("Summary:", summary)

        st.write("Chat with AI about the content:")
        user_input = st.text_input("Your message:")
        if user_input:
            ai_response = chat_with_ai(f"Based on the uploaded file, answer this question: {user_input}", uploaded_file)
            if ai_response.startswith("An error occurred:"):
                st.error(ai_response)
            else:
                st.write("AI Response:", ai_response)
