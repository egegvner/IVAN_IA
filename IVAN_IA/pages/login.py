import streamlit as st
from utils.auth import authenticate_user, login_user
import time

def login_page():
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", type="primary", use_container_width=True):
        if not username or not password:
            st.error("Both username and password are required!")
        else:
            user = authenticate_user(username, password)
            if user:
                with st.spinner("Logging you in..."):
                    login_user(user)
                    time.sleep(3)
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")