import streamlit as st
import requests
from pypdf import PdfReader

st.title("AI Study Assistant")

uploaded_file = st.file_uploader(
    "Upload PDF Notes",
    type=["pdf"]
)

pdf_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pdf_text += text

    st.success("PDF uploaded successfully!")

question = st.text_input("Ask a question about your PDF")

if st.button("Ask") and question:

    prompt = f"""
    Use the following study material to answer.

    STUDY MATERIAL:
    {pdf_text}

    QUESTION:
    {question}

    Give a clear student-friendly answer.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3:latest",
            "prompt": prompt,
            "stream": False
        }
    )

    answer = response.json()["response"]

    st.subheader("Answer")
    st.write(answer)
