import streamlit as st
import pandas as pd

# Known dataframe that will always be in the first tab
known_df = pd.DataFrame({
    "col1": [1, 2, 3],
    "col2": [4, 5, 6]
})

# Dynamic list of dataframes
dataframes = [
    pd.DataFrame({"A": [10, 20, 30]}),
    pd.DataFrame({"B": [40, 50, 60]})
]

# Create tab names: first for the known dataframe, and then for each dynamic dataframe
tab_names = ["Known DataFrame"] + [f"Tab {i+2}" for i in range(len(dataframes))]

# Create tabs
tabs = st.tabs(tab_names)

# Display the known dataframe in the first tab
with tabs[0]:
    st.dataframe(known_df)

# Display each dataframe from the dynamic list in the remaining tabs
for tab, df in zip(tabs[1:], dataframes):
    with tab:
        st.dataframe(df)
