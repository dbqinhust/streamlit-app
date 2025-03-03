import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import os
from streamlit_pdf_viewer import pdf_viewer

# Function to save uploaded PDF
def save_uploaded_file(uploaded_file):
    save_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

# Function to extract PDF info
def extract_pdf_info(file_path):
    doc = fitz.open(file_path)
    pages = []
    
    for page_num in range(len(doc)):
        text = doc[page_num].get_text("text")[:100]  # Extract first 100 characters
        link = f'<a href="?page={page_num+1}" target="_self">View Page {page_num+1}</a>'  # Clickable link
        pages.append({"Page": page_num + 1, "Extracted Text": text + "...", "Link": link})
    
    return pd.DataFrame(pages)

# Streamlit UI
st.title("PDF Viewer with Clickable Links")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    pdf_path = save_uploaded_file(uploaded_file)
    extracted_df = extract_pdf_info(pdf_path)

    # Store PDF path in session state
    st.session_state["pdf_path"] = pdf_path

    # Get selected page from query parameters
    query_params = st.experimental_get_query_params()
    selected_page = int(query_params.get("page", [1])[0])  # Default to Page 1

    # Display extracted data with clickable links
    st.write("### Extracted Data")

    # Convert DataFrame to Markdown for rendering HTML links
    def render_link(row):
        return row["Link"]

    extracted_df["Link"] = extracted_df.apply(render_link, axis=1)
    st.markdown(extracted_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Display PDF viewer
    st.write("### PDF Viewer")
    pdf_viewer(st.session_state["pdf_path"], page_number=selected_page)
