import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter

st.title("Editable DataFrame with Approve/Reject for Each Cell")

# Predefined DataFrame with 10 rows and 5 run columns (some N/A values)
data = {
    "run_1": [10, 20, 15, 5,  np.nan, 40, 50, 60, 70,  np.nan],
    "run_2": [10, np.nan, 15, 5,  25,     40, 50, 55, 70,  80],
    "run_3": [10, 20,    np.nan, 10, 25,     40, np.nan, 60, 70,  80],
    "run_4": [5,  20,    15,    5,  30,     40, 45, 60, 70,  80],
    "run_5": [10, 30,    15,    np.nan, 25, 40, 50, 60, np.nan, 80]
}

df = pd.DataFrame(data)

# Function to compute majority (mode) ignoring NaN
def compute_majority(row):
    values = [v for v in row if pd.notnull(v)]
    return Counter(values).most_common(1)[0][0] if values else np.nan

# Editable DataFrame
edited_df = df.copy()

st.markdown("""
### Instructions:
- Click on **any cell** to change its value.
- The **majority_value** column updates automatically.
""")

# Use st.data_editor to allow **direct cell editing**
edited_df = st.data_editor(edited_df, num_rows="dynamic")

# Recalculate majority value
edited_df["majority_value"] = edited_df.apply(compute_majority, axis=1)

st.subheader("Updated DataFrame")
st.dataframe(edited_df)
