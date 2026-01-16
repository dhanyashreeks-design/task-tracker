import streamlit as st
from db import *

st.set_page_config(page_title="Task Streaks", layout="centered")
init_db()

st.title("🔥 Daily Task Streaks")

new_task = st.text_input("Add a new task")
if st.button("➕ Add Task"):
    if new_task:
        add_task(new_task)
        st.success("Task added!")

st.divider()

tasks = get_tasks()

for task_id, task_name in tasks:
    current, max_streak = get_streak(task_id)

    with st.container():
        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader(task_name)
            st.progress(min(current / max(1, max_streak), 1.0))
            st.caption(f"🔥 Streak: {current} | 🏆 Best: {max_streak}")

        with col2:
            if st.button("✅ Done", key=task_id):
                complete_task(task_id)
                st.rerun()

        with st.expander("📅 View history"):
            history = get_history(task_id)
            if history:
                for h in history:
                    st.write("✅", h[0])
            else:
                st.write("No history yet")

        st.divider()
