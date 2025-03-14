import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'ID': [f'BS{i}' for i in range(1, 41)],
    'Value': [10, 25, 5, 30, 15] * 8
})

def highlight_value(val):
    return 'background-color: red' if val < 15 else 'background-color: green'

styled_df = df.style.applymap(highlight_value, subset=['Value'])
st.dataframe(styled_df)

df2 = st.data_editor(
    styled_df,
    disabled=["Value"],
    num_rows="fixed"
)