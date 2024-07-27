import streamlit as st
from pages.interview import interview_chatbot
from utils.session_state import initialize_session_state
from utils.auth import login, signup, logout
from utils.real_time_pipeline import RealTimePipeline



def main():
    st.set_page_config(page_title="AI Interview Coach", layout="wide")
    initialize_session_state()

    # Initialize real-time pipeline
    if 'pipeline' not in st.session_state:
        st.session_state.pipeline = RealTimePipeline()

    # Sidebar for authentication and navigation
    with st.sidebar:
        st.title("AI Interview Coach")
        if st.session_state.user:
            st.write(f"Welcome, {st.session_state.user}")
            if st.button("Logout"):
                logout()
        else:
            login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
            with login_tab:
                login()
            with signup_tab:
                signup()

        if st.session_state.user:
            interview_type = st.selectbox("Choose Interview Type",
                                          ["General", "Technical", "Behavioral"])
            if st.button("Start New Interview"):
                st.session_state.current_question_index = 0
                st.session_state.interview_completed = False
                st.session_state.chat_history = []

    if st.session_state.user:
        interview_chatbot(st.session_state.pipeline, interview_type)
    else:
        st.info("Please login or sign up to start your interview practice.")


if __name__ == "__main__":
    main()