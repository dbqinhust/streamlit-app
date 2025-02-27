import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

st.title("Dataframe with Cell Approval Dropdowns")

# Create a sample dataframe with 40 rows and 2 columns: Value and Notes.
df = pd.DataFrame({
    "Field": [f"Field_{i}" for i in range(1, 41)],
    "Value": [f"Value_{i}" for i in range(1, 41)],
    "Notes": [f"Notes_{i}" for i in range(1, 41)]
})

# For each column that we want to approve (here "Value" and "Notes"),
# add a corresponding approval column with a default value "Approve".
for col in ["Value", "Notes"]:
    df[f"{col}_Approval"] = "Approve"

# Build grid options using AgGrid's GridOptionsBuilder.
gb = GridOptionsBuilder.from_dataframe(df)

# Configure the approval columns to be editable dropdowns with the options.
for approval_col in ["Value_Approval", "Notes_Approval"]:
    gb.configure_column(
        approval_col,
        editable=True,
        cellEditor="agSelectCellEditor",
        cellEditorParams={"values": ["Approve", "Reject"]},
        width=150
    )

# Define a helper function to add conditional formatting:
# if the corresponding approval column equals "Reject", then style the cell in red.
def add_conditional_formatting(data_col, approval_col):
    js_code = f"""
    function(params) {{
        if (params.data['{approval_col}'] === 'Reject') {{
            return {{'color': 'red', 'fontWeight': 'bold'}};
        }} else {{
            return {{}};
        }}
    }}
    """
    gb.configure_column(data_col, cellStyle=js_code)

# Apply conditional formatting to our data columns.
add_conditional_formatting("Value", "Value_Approval")
add_conditional_formatting("Notes", "Notes_Approval")

gridOptions = gb.build()

# Display the grid using AgGrid.
grid_response = AgGrid(
    df,
    gridOptions=gridOptions,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    fit_columns_on_grid_load=True,
    enable_enterprise_modules=False,
)

st.subheader("Updated Dataframe")
st.dataframe(grid_response['data'])
