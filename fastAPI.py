import streamlit as st
import requests
from streamlit_option_menu import option_menu

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="ToDo App", layout="centered")


st.title(" ToDo Manager")


with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Create", "Read", "Update", "Delete"],
        icons=["plus", "eye", "pencil-square", "trash"],
        default_index=0
    )


if selected == "Create":
    st.subheader("Add a New Task")
    with st.form("todo_form", clear_on_submit=True):
        title = st.text_input("Title")
        description = st.text_area("Description")
        completed = st.checkbox("Completed", value=False)
        submitted = st.form_submit_button("Add ToDo")

        if submitted:
            if not title.strip():
                st.warning("Title cannot be empty.")
            else:
                response = requests.post(f"{API_URL}/todos/", json={
                    "title": title,
                    "description": description,
                    "completed": completed
                })
                if response.status_code == 200:
                    st.success(" ToDo added successfully!")
                else:
                    st.error(" Failed to add ToDo.")


elif selected == "Read":
    st.subheader(" Current Tasks")
    response = requests.get(f"{API_URL}/todos/")
    if response.status_code == 200:
        todos = response.json()
        if not todos:
            st.info("No tasks available.")
        else:
            for todo in todos:
                with st.expander(f"{todo['title']} (ID: {todo['id']})"):
                    st.write(f"**Description:** {todo['description']}")
                    st.write(f"**Completed:** {'' if todo['completed'] else ''}")
    else:
        st.error("Failed to fetch tasks.")


elif selected == "Update":
    st.subheader(" Update Tasks")
    response = requests.get(f"{API_URL}/todos/")
    if response.status_code == 200:
        todos = response.json()
        for todo in todos:
            with st.expander(f"{todo['title']} (ID: {todo['id']})"):
                new_title = st.text_input("Title", value=todo["title"], key=f"title_{todo['id']}")
                new_description = st.text_area("Description", value=todo["description"], key=f"desc_{todo['id']}")
                new_completed = st.checkbox("Completed?", value=todo["completed"], key=f"comp_{todo['id']}")

                if st.button("Update", key=f"update_{todo['id']}"):
                    res = requests.put(f"{API_URL}/todos/{todo['id']}", json={
                        "title": new_title,
                        "description": new_description,
                        "completed": new_completed
                    })
                    if res.status_code == 200:
                        st.success(" Task updated successfully! Refresh to see changes.")
                    else:
                        st.error(" Failed to update task.")
    else:
        st.error("Failed to load tasks for updating.")


elif selected == "Delete":
    st.subheader(" Delete Tasks")
    response = requests.get(f"{API_URL}/todos/")
    if response.status_code == 200:
        todos = response.json()
        for todo in todos:
            with st.expander(f"{todo['title']} (ID: {todo['id']})"):
                st.write(f"**Description:** {todo['description']}")
                st.write(f"**Completed:** {'' if todo['completed'] else ''}")
                if st.button("Delete", key=f"delete_{todo['id']}"):
                    res = requests.delete(f"{API_URL}/todos/{todo['id']}")
                    if res.status_code == 200:
                        st.success(" Task deleted! Refresh to update list.")
                    else:
                        st.error(" Failed to delete task.")
    else:
        st.error("Failed to load tasks for deletion.")
