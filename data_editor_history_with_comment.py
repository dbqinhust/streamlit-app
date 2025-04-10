import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit import session_state as ss

CURRENT_USER = "Alice"

# Initial DataFrame
initial_df = pd.DataFrame([
    {"command": "st.selectbox", "rating": 4, "is_widget": True},
    {"command": "st.balloons", "rating": 5, "is_widget": False},
    {"command": "st.time_input", "rating": 3, "is_widget": True},
])

# Initialize session state
if "df" not in ss:
    ss.df = initial_df.copy()
if "edit_log" not in ss:
    ss.edit_log = pd.DataFrame(columns=[
        "row_index", "command", "timestamp", "user",
        "old_rating", "new_rating", "comment"
    ])
if "pending_comments" not in ss:
    ss.pending_comments = {}
if "edited_cache" not in ss:
    ss.edited_cache = {}
if "submitted" not in ss:
    ss.submitted = False

# Show the data editor (only rating editable)
edited_df = st.data_editor(
    ss.df,
    column_config={
        "rating": st.column_config.NumberColumn("Rating", min_value=0, max_value=5),
        "command": st.column_config.TextColumn("Command", disabled=True),
        "is_widget": st.column_config.CheckboxColumn("Is Widget", disabled=True),
    },
    use_container_width=True,
    key="ed",
)

# Save a snapshot of edited rows to avoid loss after rerun
# if ss.ed.get("edited_rows") and not ss.submitted:
#     ss.edited_cache = ss.ed["edited_rows"].copy()

# edited_rows = ss.edited_cache
edited_rows = ss.ed["edited_rows"]
print(edited_rows)

# Show comment boxes for edited rows (only if not just submitted)
if edited_rows and not ss.submitted:
    st.markdown("### Add a comment for your rating changes")
    for row_idx_str, change_dict in edited_rows.items():
        row_idx = int(row_idx_str)
        if "rating" in change_dict:
            comment_key = f"comment_{row_idx}"
            default_comment = ss.pending_comments.get(row_idx, "")
            comment = st.text_input(
                f"Comment for `{ss.df.loc[row_idx, 'command']}` (Row {row_idx}):",
                value=default_comment,
                key=comment_key
            )
            ss.pending_comments[row_idx] = comment

# Submit button
if st.button("Submit Changes"):
    for row_idx_str, change_dict in edited_rows.items():
        row_idx = int(row_idx_str)
        if "rating" in change_dict:
            old_rating = ss.df.loc[row_idx, "rating"]
            new_rating = change_dict["rating"]
            command_value = ss.df.loc[row_idx, "command"]
            comment = ss.pending_comments.get(row_idx, "")

            log_entry = {
                "row_index": row_idx,
                "command": command_value,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "user": CURRENT_USER,
                "old_rating": old_rating,
                "new_rating": new_rating,
                "comment": comment
            }

            # Update the DataFrame and log
            ss.df.loc[row_idx, "rating"] = new_rating
            ss.edit_log = pd.concat([ss.edit_log, pd.DataFrame([log_entry])], ignore_index=True)

    # Clear everything after submission
    ss.edited_cache.clear()
    ss.ed["edited_rows"].clear()
    ss.pending_comments.clear()
    ss.submitted = True  # trigger hiding of comment boxes
    st.success("Changes submitted!")
    

# Reset the submitted flag after a clean render
if ss.submitted and not edited_rows:
    ss.submitted = False
    st.rerun()

# Display favorite command
favorite_command = ss.df.loc[ss.df["rating"].idxmax()]["command"]
st.markdown(f"Your favorite command is **{favorite_command}** 🎈")

# Display edit history
st.subheader("Edit Log with Comments")
st.dataframe(ss.edit_log.sort_values("timestamp").reset_index(drop=True))

