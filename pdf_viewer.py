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
        text = doc[page_num].get_text("text")[:100]  # Extract first 100 chars
        link = f"View Page {page_num+1}"  # The clickable link
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

    # Select a page to display
    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = 1  # Default to Page 1

    # Function to update selected page
    def update_page(page_num):
        st.session_state["selected_page"] = page_num

    # Display extracted data as a table with buttons
    st.write("### Extracted Data")

    for _, row in extracted_df.iterrows():
        col1, col2, col3 = st.columns([1, 4, 1])
        with col1:
            st.write(f"Page {row['Page']}")
        with col2:
            st.write(row["Extracted Text"])
        with col3:
            if st.button(row["Link"], key=f"btn_{row['Page']}"):
                update_page(row["Page"])  # Update page number when clicked

    # Display PDF viewer
    st.write("### PDF Viewer")
    pdf_viewer(st.session_state["pdf_path"], page_number=st.session_state["selected_page"])
