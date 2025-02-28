import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter

st.title("Editable DataFrame with Save Changes & Unique Edit History")

# Initialize session state for DataFrame, edit history, and saved changes
if "df" not in st.session_state:
    st.session_state.df = None  # Holds the generated DataFrame
if "edit_history" not in st.session_state:
    st.session_state.edit_history = []  # Stores edit logs
if "saved_df" not in st.session_state:
    st.session_state.saved_df = None  # Stores saved changes
if "tracked_changes" not in st.session_state:
    st.session_state.tracked_changes = {}  # Prevents duplicate history entries

# Function to generate the DataFrame with "field" index
def generate_dataframe():
    data = {
        "field": [f"data{i+1}" for i in range(10)],  # Index column
        "run_1": [10, 20, 15, 5,  np.nan, 40, 50, 60, 70,  np.nan],
        "run_2": [10, np.nan, 15, 5,  25,     40, 50, 55, 70,  80],
        "run_3": [10, 20,    np.nan, 10, 25,     40, np.nan, 60, 70,  80],
        "run_4": [5,  20,    15,    5,  30,     40, 45, 60, 70,  80],
        "run_5": [10, 30,    15,    np.nan, 25, 40, 50, 60, np.nan, 80]
    }
    return pd.DataFrame(data)

# Function to compute majority (mode) ignoring NaN
def compute_majority(row):
    values = [v for v in row[1:] if pd.notnull(v)]  # Exclude "field" column
    return Counter(values).most_common(1)[0][0] if values else np.nan

# "Run" button to generate the DataFrame
if st.button("Run"):
    st.session_state.df = generate_dataframe()
    st.session_state.edit_history = []  # Reset history on new run
    st.session_state.saved_df = None  # Clear saved state
    st.session_state.tracked_changes = {}  # Reset tracked changes

# Display DataFrame only after running
if st.session_state.df is not None:
    st.markdown("### Instructions:")
    st.markdown("- Click on **any cell** to edit its value.")
    st.markdown("- Click **'Save Changes'** to store your edits and recalculate the majority value.")
    st.markdown("- **Edit history** is tracked below (duplicates are prevented).")

    # Editable DataFrame
    edited_df = st.data_editor(st.session_state.df.copy(), num_rows="dynamic")

    # Compare original vs edited values and log only NEW changes
    for row_idx in range(len(st.session_state.df)):
        for col in st.session_state.df.columns:
            if col != "field":  # Don't track changes to the "field" column
                old_value = st.session_state.df.at[row_idx, col]
                new_value = edited_df.at[row_idx, col]

                if old_value != new_value and pd.notnull(new_value):
                    change_key = f"{row_idx}_{col}"  # Unique key for each change

                    # Only add the change if it's new (not already tracked)
                    if change_key not in st.session_state.tracked_changes:
                        st.session_state.edit_history.append({
                            "Field": edited_df.at[row_idx, "field"],
                            "Column": col,
                            "Old Value": old_value,
                            "New Value": new_value
                        })
                        st.session_state.tracked_changes[change_key] = new_value  # Track the change

    # Save Changes Button
    if st.button("Save Changes"):
        edited_df["majority_value"] = edited_df.apply(compute_majority, axis=1)
        st.session_state.saved_df = edited_df.copy()  # Store saved changes

# Display Saved DataFrame (after clicking "Save Changes")
    if st.session_state.saved_df is not None:
        st.subheader("Final Updated DataFrame (After Saving)")
        st.dataframe(st.session_state.saved_df)

    # Display Edit History
    if st.session_state.edit_history:
        st.subheader("Edit History (No Duplicates)")
        history_df = pd.DataFrame(st.session_state.edit_history)
        st.dataframe(history_df)
    else:
        st.info("No edits have been made yet.")
