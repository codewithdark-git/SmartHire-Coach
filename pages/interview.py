import streamlit as st


def interview_chatbot(pipeline, interview_type):
    st.header(f"{interview_type} Interview Practice")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0

    if 'interview_completed' not in st.session_state:
        st.session_state.interview_completed = False

    questions = pipeline.fetch_questions(interview_type)

    if st.session_state.current_question_index < len(questions) and not st.session_state.interview_completed:
        current_question = questions[st.session_state.current_question_index]

        if not st.session_state.chat_history or st.session_state.chat_history[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                st.markdown(current_question['question'])
                for i, choice in enumerate(current_question['choices'], 1):
                    st.markdown(f"{i}. {choice}")
            st.session_state.chat_history.append({"role": "assistant", "content": current_question['question']})

        user_answer = st.chat_input("Your answer")

        if user_answer:
            with st.chat_message("user"):
                st.markdown(user_answer)
            st.session_state.chat_history.append({"role": "user", "content": user_answer})

            feedback = pipeline.process_answer(current_question, user_answer)
            with st.chat_message("assistant"):
                st.markdown(feedback)
            st.session_state.chat_history.append({"role": "assistant", "content": feedback})

            st.session_state.current_question_index += 1

    if st.session_state.current_question_index >= len(questions):
        st.session_state.interview_completed = True

    if st.session_state.interview_completed:
        with st.chat_message("assistant"):
            overall_feedback = pipeline.generate_overall_feedback(st.session_state.chat_history)
            st.markdown(overall_feedback)
        st.button("Start New Interview", on_click=reset_interview())

def reset_interview():
    st.session_state.current_question_index = 0
    st.session_state.interview_completed = False
    st.session_state.chat_history = []
    st.rerun()
