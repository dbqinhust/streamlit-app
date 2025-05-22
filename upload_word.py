import streamlit as st
from docx import Document
import io

st.title("Upload and Extract Text from Word Document")

uploaded_file = st.file_uploader("Upload a .docx file", type="docx")

if uploaded_file is not None:
    # Read the file into a Document object
    doc = Document(io.BytesIO(uploaded_file.read()))
    
    # Extract all text
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    
    text_output = "\n".join(full_text)
    
    st.subheader("Extracted Text:")
    st.text_area("Document Text", text_output, height=400)
