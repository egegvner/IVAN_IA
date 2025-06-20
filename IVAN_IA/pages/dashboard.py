import streamlit as st
import datetime
from db.database import execute_query, execute_update
from utils.planner import compute_revision_sessions
from utils.helpers import WEEKDAYS

def dashboard_page(user):
    st.markdown(
        """
        <style>
        /* Hide default Streamlit menu and footer */
        #MainMenu {visibility: hidden;} 
        footer {visibility: hidden;} 
        /* Set minimal font and spacing */
        html, body, .block-container {font-family: 'Helvetica Neue', sans-serif; padding: 1rem 2rem;}
        .section-header {margin-top: 2rem; margin-bottom: 1rem; font-weight: 600; font-size:1.2rem;}
        </style>
        """, 
        unsafe_allow_html=True
    )

    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif 12 <= current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    st.title(f"{greeting}, {user['username']}!", anchor=False)
    user_id = user['id']

    st.markdown('<div class="section-header">🗓️ Weekly Availability</div>', unsafe_allow_html=True)
    existing = execute_query(
        "SELECT day FROM availability WHERE user_id = ? AND is_available = 1", (user_id,)
    )
    default_days = [r['day'] for r in existing]
    selected_days = st.multiselect(
        "Select days you can study:", WEEKDAYS, default=default_days, key='avail_multiselect'
    )
    if st.button("Save Availability 🏷️"):
        execute_update("DELETE FROM availability WHERE user_id = ?", (user_id,))
        for day in WEEKDAYS:
            is_avail = 1 if day in selected_days else 0
            execute_update(
                "INSERT INTO availability (user_id, day, is_available) VALUES (?, ?, ?)",
                (user_id, day, is_avail)
            )
        st.success("Availability updated!")

    st.markdown("---")

    st.markdown('<div class="section-header">✏️ Subjects & Exams</div>', unsafe_allow_html=True)
    with st.expander("Add a new subject", expanded=False):
        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        with col1:
            subj_name = st.text_input("Subject Name", key="subj_name_input")
        with col2:
            exam_date = st.date_input("Exam Date", min_value=datetime.date.today(), key="exam_date_input")
        with col3:
            priority = st.slider("Priority", 1, 10, 5, key="priority_input")
        with col4:
            if st.button("Add ➕", key="add_subject_btn"):
                if subj_name:
                    execute_update(
                        "INSERT INTO subjects (user_id, subject_name, exam_date, priority) VALUES (?, ?, ?, ?)",
                        (user_id, subj_name, exam_date.isoformat(), priority)
                    )
                    st.rerun()
                else:
                    st.error("Enter a subject name.")

    subjects = execute_query(
        "SELECT id, subject_name, exam_date, priority FROM subjects WHERE user_id = ? ORDER BY exam_date", (user_id,)
    )
    if subjects:
        st.markdown('<div class="section-header">📚 Your Subjects</div>', unsafe_allow_html=True)
        for s in subjects:
            cols = st.columns([3, 2, 1, 1])
            cols[0].markdown(f"**{s['subject_name']}**")
            cols[1].markdown(f"{s['exam_date']}")
            cols[2].markdown(f"Priority: {s['priority']}")
            if cols[3].button("🗑️", key=f"del_{s['id']}"):
                execute_update("DELETE FROM subjects WHERE id = ?", (s['id'],))
                st.rerun()
    else:
        st.info("No subjects yet. Add one above!")

    st.markdown("---")

    st.markdown('<div class="section-header">🗓️ Revision Calendar</div>', unsafe_allow_html=True)
    avail_rows = execute_query(
        "SELECT day FROM availability WHERE user_id = ? AND is_available = 1", (user_id,)
    )
    available_days = {r['day'] for r in avail_rows}
    subjects = execute_query(
        "SELECT id, subject_name, exam_date FROM subjects WHERE user_id = ?", (user_id,)
    )

    all_sessions = []
    for s in subjects:
        exam_dt = datetime.datetime.fromisoformat(s['exam_date']).date()
        sessions = compute_revision_sessions(s['id'], exam_dt, available_days)
        for _sid, date, label in sessions:
            all_sessions.append((s['subject_name'], date, label))

    if all_sessions:
        calendar = {day: [] for day in WEEKDAYS}
        for subj_name, date, label in all_sessions:
            calendar[date.strftime('%A')].append(f"{subj_name}: {label}")
        cols = st.columns(7)
        for idx, day in enumerate(WEEKDAYS):
            with cols[idx]:
                st.markdown(f"**{day[:3]}**")
                for item in calendar[day]:
                    st.markdown(f"- {item}")
    else:
        st.info("No revision sessions. Ensure you have subjects and availability set.")
