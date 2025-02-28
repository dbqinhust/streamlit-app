import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter

st.title("Editable DataFrame with Edit History Tracking")

# Predefined DataFrame with 10 rows and 5 run columns (some N/A values)
data = {
    "run_1": [10, 20, 15, 5,  np.nan, 40, 50, 60, 70,  np.nan],
    "run_2": [10, np.nan, 15, 5,  25,     40, 50, 55, 70,  80],
    "run_3": [10, 20,    np.nan, 10, 25,     40, np.nan, 60, 70,  80],
    "run_4": [5,  20,    15,    5,  30,     40, 45, 60, 70,  80],
    "run_5": [10, 30,    15,    np.nan, 25, 40, 50, 60, np.nan, 80]
}

df = pd.DataFrame(data)

# Initialize session state for edit history
if "edit_history" not in st.session_state:
    st.session_state.edit_history = []

# Function to compute majority (mode) ignoring NaN
def compute_majority(row):
    values = [v for v in row if pd.notnull(v)]
    return Counter(values).most_common(1)[0][0] if values else np.nan

# Editable DataFrame
st.markdown("### Instructions:")
st.markdown("- Click on **any cell** to edit its value.")
st.markdown("- The **majority_value** updates automatically.")
st.markdown("- **History of edits** is tracked below.")

edited_df = st.data_editor(df.copy(), num_rows="dynamic")

# Compare original vs edited values and log changes
for row_idx in range(len(df)):
    for col in df.columns:
        old_value = df.at[row_idx, col]
        new_value = edited_df.at[row_idx, col]

        if old_value != new_value and pd.notnull(new_value):
            st.session_state.edit_history.append({
                "Row": row_idx + 1,
                "Column": col,
                "Old Value": old_value,
                "New Value": new_value
            })

# Recalculate majority after edits
edited_df["majority_value"] = edited_df.apply(compute_majority, axis=1)

st.subheader("Updated DataFrame")
st.dataframe(edited_df)

# Display edit history
if st.session_state.edit_history:
    st.subheader("Edit History")
    history_df = pd.DataFrame(st.session_state.edit_history)
    st.dataframe(history_df)
else:
    st.info("No edits have been made yet.")
