import streamlit as st

# Define your table manually
html = """
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
"""

# Display in Streamlit
st.markdown(html, unsafe_allow_html=True)
