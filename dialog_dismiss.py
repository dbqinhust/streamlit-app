import streamlit as st

# Create a flag in session state to track if the dialog was opened
if "dialog_open" not in st.session_state:
    st.session_state.dialog_open = False

if "dialog_saved" not in st.session_state:
    st.session_state.dialog_saved = False

# Button to open the dialog
if st.button("Open Dialog"):
    st.session_state.dialog_open = True
    st.session_state.dialog_saved = False  # Reset save status

# If dialog is open
if st.session_state.dialog_open:
    with st.dialog("Example Dialog"):
        st.write("Edit your information here.")
        
        if st.button("Save"):
            st.session_state.dialog_saved = True
            st.session_state.dialog_open = False  # Close dialog
            st.success("Saved successfully!")

# Check if user dismissed without saving
if not st.session_state.dialog_open and not st.session_state.dialog_saved:
    st.warning("Dialog dismissed without saving!")
