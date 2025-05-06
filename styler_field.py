import streamlit as st
import pandas as pd

# Create 2×2 DataFrame: empty + color labels
df = pd.DataFrame([
    ["", "Red"],
    ["", "Yellow"]
])

# Apply background color only to first column based on value in second column
def color_first_column(row):
    if row[1] == "Red":
        return ["background-color: lightcoral", ""]
    elif row[1] == "Yellow":
        return ["background-color: khaki", ""]
    return ["", ""]

# Apply styling row-wise
styled = df.style.apply(color_first_column, axis=1)

# Hide index and column headers (requires pandas ≥ 2.0)
styled = styled.hide(axis="index").hide(axis="columns")

# Display in Streamlit
st.dataframe(styled, use_container_width=True)
