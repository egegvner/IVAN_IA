import streamlit as st
from db.database import init_db
from utils.auth import get_current_user, logout_user
from pages.login import login_page
from pages.register import register_page
from pages.dashboard import dashboard_page
from config import PAGE_TITLE, PAGE_ICON, LAYOUT, INITIAL_SIDEBAR_STATE

def main():
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT,
        initial_sidebar_state=INITIAL_SIDEBAR_STATE
    )

    init_db()
    user = get_current_user()

    if user:
        st.sidebar.markdown(f"### Welcome, {user['username']} 👋")
        nav_choice = st.sidebar.radio("Navigate to", ["Dashboard", "Logout"], key="nav_user")

        if nav_choice == "Dashboard":
            dashboard_page(user)
        elif nav_choice == "Logout":
            logout_user()
            st.experimental_rerun()
    else:
        st.write("# Study Planner")
        choice = st.radio("", ["Login", "Register"])

        if choice == "Login":
            login_page()
        elif choice == "Register":
            register_page()

if __name__ == "__main__":
    main()
