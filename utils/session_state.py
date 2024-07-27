# utils/session_state.py
import streamlit as st
def initialize_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'interview_completed' not in st.session_state:
        st.session_state.interview_completed = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []