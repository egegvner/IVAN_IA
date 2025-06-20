import streamlit as st
from utils.auth import register_user, login_user
import time

def register_page():
    username = st.text_input("Choose a username", key="reg_username")
    password = st.text_input("Choose a password", type="password", key="reg_password")
    confirm_password = st.text_input("Confirm password", type="password", key="reg_confirm_password")

    if st.button("Register", type="primary", use_container_width=True):
        if not username or not password or not confirm_password:
            st.error("All fields are required! 🚨")
        elif password != confirm_password:
            st.error("Passwords do not match. Please try again. 🔄")
        else:
            success = register_user(username, password)
            if success:
                st.success(f"Account created successfully, {username}! Welcome aboard! 🎉")
                user = {'id': None, 'username': username}
                with st.spinner("Logging you in..."):
                    login_user({'id': None, 'username': username})
                    time.sleep(3)
                st.rerun()
            else:
                st.error("Username already taken. Try a different one. 🤔")