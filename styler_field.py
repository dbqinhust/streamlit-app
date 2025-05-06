import streamlit as st

html = """
<div style="display: flex; justify-content: flex-end;">
  <table style="border-collapse: collapse;">
    <tr>
      <td style="background-color: lightcoral; padding: 8px; width: 100px;"></td>
      <td style="padding: 8px;">Red</td>
    </tr>
    <tr>
      <td style="background-color: khaki; padding: 8px;"></td>
      <td style="padding: 8px;">Yellow</td>
    </tr>
  </table>
</div>
"""

st.markdown(html, unsafe_allow_html=True)
