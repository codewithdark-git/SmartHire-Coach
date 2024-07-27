import streamlit as st
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # In a real application, you'd verify against a secure user store
        if username and password:  # Simplified check for demo
            st.session_state.user = username
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

def signup():
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    if st.button("Sign Up"):
        # In a real application, you'd add the user to a secure user store
        if username and password:  # Simplified check for demo
            st.session_state.user = username
            st.success("Account created successfully! You're now logged in.")
        else:
            st.error("Please provide both username and password.")

def logout():
    st.session_state.user = None
    st.session_state.current_question_index = 0
    st.session_state.interview_completed = False
    st.session_state.chat_history = []
    st.info("Logged out successfully.")