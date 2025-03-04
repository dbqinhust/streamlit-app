import streamlit as st
import pandas as pd
import os
import time

# -------------------------------
# Configuration for Cache Folder
# -------------------------------
CACHE_DIR = "cache_files"     # Folder to store cached PDFs
CACHE_TTL = 600               # TTL in seconds (e.g. 600s = 10 minutes)

# Ensure the cache folder exists
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Function to remove cache files older than TTL
def cleanup_cache():
    now = time.time()
    for filename in os.listdir(CACHE_DIR):
        filepath = os.path.join(CACHE_DIR, filename)
        if os.path.isfile(filepath):
            creation_time = os.path.getctime(filepath)
            if now - creation_time > CACHE_TTL:
                os.remove(filepath)

cleanup_cache()

st.title("PDF Cache & Direct Link Example")

# -------------------------------
# Upload and Cache the PDF
# -------------------------------
if "pdf_cache_filename" not in st.session_state:
    st.session_state["pdf_cache_filename"] = None

if st.session_state["pdf_cache_filename"] is None:
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file is not None:
        # Create a unique filename with timestamp
        cached_filename = f"{int(time.time())}_{uploaded_file.name}"
        cached_path = os.path.join(CACHE_DIR, cached_filename)
        with open(cached_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state["pdf_cache_filename"] = cached_filename

# -------------------------------
# Generate Direct Links with Page Numbers
# -------------------------------
if st.session_state["pdf_cache_filename"] is not None:
    # For this example, assume 5 pages
    pages = list(range(1, 6))
    
    # Build the base URL assuming cached files are accessible at 'cache_files/<filename>'
    base_url = f"{CACHE_DIR}/{st.session_state['pdf_cache_filename']}"
    
    st.write("### PDF Pages with Direct Links")
    # Instead of using a table, output each link individually
    for p in pages:
        link_html = f'<a href="{base_url}#page={p}" target="_blank">View Page {p}</a>'
        st.markdown(link_html, unsafe_allow_html=True)
else:
    st.info("Please upload a PDF file.")

