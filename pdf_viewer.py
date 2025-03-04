import streamlit as st
import pandas as pd
import os
from streamlit_pdf_viewer import pdf_viewer

# Dummy PDF file for testing
PDF_PATH = "example.pdf"  # Replace with an uploaded file if needed

# Store PDF in session state
st.session_state["pdf_path"] = PDF_PATH

# Sample DataFrame with page numbers
data = {
    "Page": [1, 2, 3, 4, 5],  # Known page numbers
}
df = pd.DataFrame(data)

# Generate clickable links that modify the URL parameter
df["Link"] = df["Page"].apply(lambda p: f'<a href="?page={p}" target="_self">View Page {p}</a>')

# Display DataFrame with clickable links
st.write("### PDF Pages with Links")
st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

# Get selected page from URL query parameter
query_params = st.experimental_get_query_params()
selected_page = int(query_params.get("page", [1])[0])  # Default to Page 1

# Show PDF viewer for selected page
if "pdf_path" in st.session_state:
    st.write(f"### Viewing Page {selected_page}")
    pdf_viewer(st.session_state["pdf_path"], page_number=selected_page)

