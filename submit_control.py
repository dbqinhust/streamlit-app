import streamlit as st
import pandas as pd

# Initialize the session state on first run
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Sample editable data
data = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Score": [10, 20, 30]
})

# Only show the data_editor if not submitted
if not st.session_state.submitted:
    edited_data = st.data_editor(data, key="editor")
    if st.button("Calculate"):
        # You can modify the edited data here
        df = pd.DataFrame(st.session_state.editor)
        df["Double Score"] = df["Score"] * 2
        st.session_state.result = df
        st.session_state.submitted = True
else:
    # Show the result table instead of the editor
    st.dataframe(st.session_state.result)
    if st.button("Reset"):
        st.session_state.submitted = False
        st.session_state.result = None
