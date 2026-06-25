import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# Page Config
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚"
)

st.title("📚 AI Study Assistant with PDF")

# API Key Input
api_key = st.text_input(
    "Enter Gemini API Key",
    type="password"
)

# PDF Upload
uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

# Extract Text Function
def extract_text_from_pdf(pdf_file):
    text = ""

    pdf_reader = PdfReader(pdf_file)

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

# Question Input
question = st.text_area(
    "Ask a question about the PDF"
)

# Ask Button
if st.button("Generate Answer"):

    if not api_key:
        st.warning("Please enter your Gemini API Key.")

    elif uploaded_file is None:
        st.warning("Please upload a PDF.")

    elif not question.strip():
        st.warning("Please enter a question.")

    else:
        try:
            # Configure Gemini
            genai.configure(api_key=api_key)

            # Extract PDF Text
            pdf_text = extract_text_from_pdf(uploaded_file)

            # Gemini Model
            model = genai.GenerativeModel(
                "models/gemini-2.5-flash"
            )

            # Prompt
            prompt = f"""
            You are an AI Study Assistant.

            Study Material:
            {pdf_text}

            Question:
            {question}

            Give a clear and detailed answer based only on the PDF content.
            """

            # Generate Response
            with st.spinner("Analyzing PDF..."):
                response = model.generate_content(prompt)

            # Display Answer
            st.subheader("📖 Answer")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Powered by Gemini 2.5 Flash")
