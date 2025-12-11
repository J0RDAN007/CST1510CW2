import streamlit as st
from db_manager import DatabaseManager
import os

st.set_page_config(page_title="Login", layout="centered")

# Check if user is already logged in
if 'logged_in' in st.session_state and st.session_state.logged_in:
    st.info(f"You are already logged in as {st.session_state.username}")
    if st.button("Go to Dashboard"):
        st.switch_page("app.py")
    st.stop()

st.title("Login")

# Initialize database
db = DatabaseManager()

# Create tabs
tab1, tab2 = st.tabs(["Login", "Register"])

# Login tab
with tab1:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if db.verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = db.get_user_role(username)
                st.success(f"Welcome {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password")

# Register tab
with tab2:
    with st.form("register_form"):
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        role = st.selectbox("Role", ["user", "admin", "cybersecurity", "it_operations", "data_science"])
        submit = st.form_submit_button("Register")
        
        if submit:
            if new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                if db.register_user(new_username, new_password, role):
                    st.success(f"User {new_username} created!")
                else:
                    st.error("Username already exists")

# Navigation
st.markdown("---")
if st.button("← Back to Home"):
    st.switch_page("app.py")