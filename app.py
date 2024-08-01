# main.py
import streamlit as st
from pages.interview import interview_chatbot, reset_interview
from utils.session_state import initialize_session_state
from utils.auth import login, signup, logout
from utils.real_time_pipeline import RealTimePipeline


def main():
    st.set_page_config(page_title="AI Interview Coach", layout="wide")

    # Initialize real-time pipeline
    if 'pipeline' not in st.session_state:
        st.session_state.pipeline = RealTimePipeline()

    # Sidebar for navigation
    with st.sidebar:
        st.title("AI Interview Coach")
        # Uncomment the following lines for authentication feature
        # if st.session_state.user:
        #     st.write(f"Welcome, {st.session_state.user}")
        #     if st.button("Logout"):
        #         logout()
        # else:
        #     login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
        #     with login_tab:
        #         login()
        #     with signup_tab:
        #         signup()

    interview_type = st.selectbox("Choose Interview Type", ["General", "Technical"])
    # Uncomment the following line if using user authentication
    # if st.session_state.user:
    interview_chatbot(st.session_state.pipeline, interview_type)
    st.button("Start New Interview", on_click=reset_interview())


if __name__ == "__main__":
    main()