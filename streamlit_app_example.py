import streamlit as st
import pandas as pd
import random
from collections import Counter

st.title("Dynamic Data Generation & Approval")

# --------------------------
# Function to Generate Data
# --------------------------
def generate_data():
    # Define sample values and notes.
    possible_values = ['A', 'B', 'C']
    possible_notes = ['Note1', 'Note2', 'Note3']

    # Define fields and their corresponding numbers.
    fields = ['field1', 'field2', 'field3', 'field4', 'field5']
    field_numbers = [1, 2, 3, 4, 5]

    dfs = []
    for run in range(5):
        data = {
            'field': fields,
            'field_number': field_numbers,
            'value': [random.choice(possible_values) for _ in fields],
            'notes': [random.choice(possible_notes) for _ in fields],
            'run': [run] * len(fields)  # Each row gets the same run number.
        }
        dfs.append(pd.DataFrame(data))
    
    # Combine and pivot the data so that each unique (field, field_number) is a row.
    combined_df = pd.concat(dfs, ignore_index=True)
    pivot_df = combined_df.pivot(index=['field', 'field_number'], columns='run')
    # Flatten the MultiIndex (e.g., ('value', 1) becomes 'value_1')
    pivot_df.columns = [f'{col[0]}_{col[1]}' for col in pivot_df.columns]
    pivot_df = pivot_df.reset_index()
    return pivot_df

# --------------------------
# Generate Data via a Button
# --------------------------
if st.button("Run"):
    # Store the generated data in session_state so it persists.
    st.session_state.pivot_df = generate_data()

# If data has not been generated yet, ask the user to click "Run".
if "pivot_df" not in st.session_state:
    st.write("Click the 'Run' button to generate data.")
else:
    pivot_df = st.session_state.pivot_df

    st.subheader("Original Pivoted DataFrame")
    st.dataframe(pivot_df)

    # --------------------------
    # Create Dropdowns for Each Run (Displayed as a Header Row)
    # --------------------------
    st.subheader("Select Approval for Each Run")
    cols = st.columns(5)
    run_status = {}
    for i in range(5):
        with cols[i]:
            run_status[i] = st.selectbox(
                f"Run {i}",
                options=["Approve", "Reject"],
                index=0,  # Default is Approve
                key=f"run{i}"
            )
    
    # Determine approved runs based on dropdown selections.
    st.write(run_status)
    approved_runs = [i for i, status in run_status.items() if status == "Approve"]
    st.write(approved_runs)
    # --------------------------
    # Function to Recalculate the Majority Value
    # --------------------------
    def calculate_majority(df, approved_runs):
        """
        Calculates the majority (mode) value from the approved run 'value' columns.
        """
        if not approved_runs:
            df['majority_value'] = None
            return df

        def majority_value(row):
            values = [row[f'value_{i}'] for i in approved_runs if f'value_{i}' in row]
            st.write(values)
            if not values:
                return None
            return Counter(values).most_common(1)[0][0]
        
        df['majority_value'] = df.apply(majority_value, axis=1)
        return df

    # --------------------------
    # Update the DataFrame Based on Approval
    # --------------------------
    df_updated = pivot_df.copy()

    # For each run, drop the columns if that run is rejected.
    for i in range(5):
        if i not in approved_runs:
            if f'value_{i}' in df_updated.columns:
                df_updated.drop(columns=[f'value_{i}'], inplace=True)
            if f'notes_{i}' in df_updated.columns:
                df_updated.drop(columns=[f'notes_{i}'], inplace=True)
    
    # Recalculate the majority value using only the approved runs.
    df_updated = calculate_majority(df_updated, approved_runs)

    st.subheader("Updated DataFrame Based on Approvals")
    st.dataframe(df_updated)
