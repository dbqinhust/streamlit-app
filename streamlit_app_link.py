import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
from collections import Counter

st.title("Dynamic Data Generation & Approval with Clickable S3 Link")

# --------------------------
# Function to Generate Data
# --------------------------
def generate_data():
    possible_values = ['A', 'B', 'C']
    possible_notes = ['Note1', 'Note2', 'Note3']
    fields = ['field1', 'field2', 'field3', 'field4', 'field5']
    field_numbers = [1, 2, 3, 4, 5]

    dfs = []
    for run in range(1, 6):
        data = {
            'field': fields,
            'field_number': field_numbers,
            'value': [random.choice(possible_values) for _ in fields],
            'notes': [random.choice(possible_notes) for _ in fields],
            'run': [run] * len(fields)
        }
        dfs.append(pd.DataFrame(data))
    
    combined_df = pd.concat(dfs, ignore_index=True)
    pivot_df = combined_df.pivot(index=['field', 'field_number'], columns='run')
    pivot_df.columns = [f'{col[0]}_{col[1]}' for col in pivot_df.columns]
    pivot_df = pivot_df.reset_index()

    # Add a clickable hyperlink column (HTML)
    pivot_df["s3_link"] = pivot_df.apply(
        lambda row: f"<a href='https://s3.amazonaws.com/mybucket/{row['field']}' target='_blank'>Link</a>", axis=1
    )
    return pivot_df

# --------------------------
# Generate Data via a Button
# --------------------------
if st.button("Run"):
    st.session_state.pivot_df = generate_data()

if "pivot_df" not in st.session_state:
    st.write("Click the 'Run' button to generate data.")
else:
    pivot_df = st.session_state.pivot_df

    st.subheader("Original Pivoted DataFrame (Clickable Links)")
    # Create the HTML table
    html_table = pivot_df.to_html(escape=False, index=False)
    # Use components.html to embed the table in an iframe with scrolling.
    components.html(
        f"""
        <div style="height: 400px; overflow-y: auto;">
            {html_table}
        </div>
        """,
        height=400,
        scrolling=True
    )

    st.subheader("Select Approval for Each Run")
    cols = st.columns(5)
    run_status = {}
    for i in range(1, 6):
        with cols[i - 1]:
            run_status[i] = st.selectbox(
                f"Run {i}",
                options=["Approve", "Reject"],
                index=0,
                key=f"run{i}"
            )
    
    approved_runs = [i for i, status in run_status.items() if status == "Approve"]

    def calculate_majority(df, approved_runs):
        if not approved_runs:
            df['majority_value'] = None
            return df

        def majority_value(row):
            values = [row[f'value_{i}'] for i in approved_runs if f'value_{i}' in row]
            if not values:
                return None
            return Counter(values).most_common(1)[0][0]
        
        df['majority_value'] = df.apply(majority_value, axis=1)
        return df

    df_updated = pivot_df.copy()
    for i in range(1, 6):
        if i not in approved_runs:
            if f'value_{i}' in df_updated.columns:
                df_updated.drop(columns=[f'value_{i}'], inplace=True)
            if f'notes_{i}' in df_updated.columns:
                df_updated.drop(columns=[f'notes_{i}'], inplace=True)

    df_updated = calculate_majority(df_updated, approved_runs)

    st.subheader("Updated DataFrame Based on Approvals (Clickable Links)")
    html_table_updated = df_updated.to_html(escape=False, index=False)
    components.html(
        f"""
        <div style="height: 400px; overflow-y: auto;">
            {html_table_updated}
        </div>
        """,
        height=400,
        scrolling=True
    )
