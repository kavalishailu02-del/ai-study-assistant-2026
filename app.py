import streamlit as st
import requests
from pypdf import PdfReader

st.set_page_config(page_title="AI Study Assistant")

st.title("📚 AI Study Assistant")

# ---------------------------
# MODE SELECTION
# ---------------------------
mode = st.radio(
    "Choose AI Mode",
    ["Local (Ollama)", "Cloud (BYOK)"]
)

# ---------------------------
# LANGUAGE (simple demo)
# ---------------------------
lang = st.selectbox("Language", ["English", "Hindi", "Telugu"])

# ---------------------------
# PDF UPLOAD
# ---------------------------
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

pdf_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text

    st.success("PDF Loaded Successfully")

# ---------------------------
# QUESTION INPUT
# ---------------------------
question = st.text_input("Ask your question")

# ---------------------------
# RESPONSE LOGIC
# ---------------------------
if st.button("Ask") and question:

    final_prompt = f"""
    Language: {lang}

    Use this study material:
    {pdf_text}

    Question:
    {question}
    """

    # ---------------------------
    # LOCAL MODE (OLLAMA)
    # ---------------------------
    if mode == "Local (Ollama)":

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3:latest",
                    "prompt": final_prompt,
                    "stream": False
                }
            )

            answer = response.json()["response"]
            st.subheader("Answer")
            st.write(answer)

        except Exception:
            st.error("❌ Local Ollama not available. Run on your laptop.")

    # ---------------------------
    # CLOUD MODE (BYOK)
    # ---------------------------
    else:
        api_key = st.text_input("Enter OpenAI API Key", type="password")

        if api_key:

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "user", "content": final_prompt}
                ]
            }

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )

            result = response.json()
            answer = result["choices"][0]["message"]["content"]

            st.subheader("Answer")
            st.write(answer)
