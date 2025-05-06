import streamlit as st

html = """
<div style="display: flex; justify-content: flex-end; gap: 30px;">

  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 20px; height: 20px; background-color: red; border-radius: 50%;"></div>
    <span>Red</span>
  </div>

  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 20px; height: 20px; background-color: yellow; border-radius: 50%; border: 1px solid #ccc;"></div>
    <span>Yellow</span>
  </div>

</div>
"""

st.markdown(html, unsafe_allow_html=True)
