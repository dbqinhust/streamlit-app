import streamlit as st
from docx import Document
import io
import openai
import os

# Set your OpenAI key here or via environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # Recommended way

st.title("Word Document Summarizer")

uploaded_file = st.file_uploader("Upload a Word (.docx) file", type="docx")

if uploaded_file is not None:
    # Extract text from Word file
    doc = Document(io.BytesIO(uploaded_file.read()))
    full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

    st.subheader("Extracted Text")
    st.text_area("Document Content", full_text, height=300)

    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",  # or "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
                    {"role": "user", "content": f"Please summarize the following document:\n\n{full_text}"}
                ],
                temperature=0.5
            )
            summary = response.choices[0].message.content
            st.subheader("Summary")
            st.write(summary)

