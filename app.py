import streamlit as st
import requests
from pypdf import PdfReader
from google import genai

st.set_page_config(page_title="AI Study Assistant")

st.title("📚 AI Study Assistant")

# -----------------------------
# MODE SELECTION
# -----------------------------
mode = st.radio("Choose AI Mode", ["Local (Ollama)", "Cloud (Gemini)"])

# -----------------------------
# LANGUAGE SELECTION
# -----------------------------
lang = st.selectbox("Language", ["English", "Hindi", "Telugu"])

# -----------------------------
# PDF UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

pdf_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text

    st.success("PDF Loaded Successfully")

# -----------------------------
# QUESTION INPUT
# -----------------------------
question = st.text_input("Ask your question")

# -----------------------------
# GENERATE BUTTON
# -----------------------------
if st.button("Ask") and question:

    final_prompt = f"""
Language: {lang}

Use this study material:
{pdf_text}

Question:
{question}

Give a simple student-friendly answer.
"""

    # -------------------------
    # LOCAL MODE (OLLAMA)
    # -------------------------
    if mode == "Local (Ollama)":

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3:latest",
                    "prompt": final_prompt,
                    "stream": False
                },
                timeout=120
            )

            result = response.json()

            if "response" in result:
                st.subheader("Answer")
                st.write(result["response"])
            else:
                st.error("Invalid Ollama response")
                st.json(result)

        except Exception as e:
            st.error(f"Ollama Error: {e}")

    # -------------------------
    # CLOUD MODE (GEMINI)
    # -------------------------
    else:

        api_key = st.text_input("Enter Gemini API Key", type="password")

        if api_key:

            try:
                from google import genai

            client = genai.Client(api_key=api_key)

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=final_prompt
            )

                st.subheader("Answer")
                st.write(response.text)

            except Exception as e:
                st.error(f"Gemini Error: {e}")

