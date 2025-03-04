import streamlit as st
import pandas as pd
import os
from streamlit_pdf_viewer import pdf_viewer

# Upload a PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    # Save the uploaded PDF in session state
    pdf_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.session_state["pdf_path"] = pdf_path

# Ensure PDF is stored in session
if "pdf_path" in st.session_state:
    PDF_PATH = st.session_state["pdf_path"]

    # Sample DataFrame with page numbers
    data = {
        "Page": [1, 2, 3, 4, 5],  # Known page numbers
    }
    df = pd.DataFrame(data)

    # Generate clickable links using Streamlit query parameters
    df["Link"] = df["Page"].apply(lambda p: f'<a href="?page={p}" target="_self">View Page {p}</a>')

    # Display DataFrame with clickable links
    st.write("### PDF Pages with Links")
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # ✅ Correct way to read query parameters (No TypeError)
    query_params = st.query_params
    selected_page = int(query_params.get("page", [1])[0])  # Default to Page 1

    # Show PDF viewer for selected page
    st.write(f"### Viewing Page {selected_page}")
    pdf_viewer(PDF_PATH, render_page_number=selected_page)


