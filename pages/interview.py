import streamlit as st


def interview_chatbot(pipeline, interview_type):
    st.header(f"{interview_type} Interview Practice")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0

    if 'waiting_for_follow_up' not in st.session_state:
        st.session_state.waiting_for_follow_up = False

    questions = pipeline.fetch_questions(interview_type)

    if st.session_state.current_question_index < len(questions):
        current_question = questions[st.session_state.current_question_index]

        if not st.session_state.waiting_for_follow_up:
            if not st.session_state.chat_history or st.session_state.chat_history[-1]["role"] != "assistant":
                with st.chat_message("assistant"):
                    st.markdown(current_question['question'])
                st.session_state.chat_history.append({"role": "assistant", "content": current_question['question']})

            user_answer = st.chat_input("Your answer")

            if user_answer:
                with st.chat_message("user"):
                    st.markdown(user_answer)
                st.session_state.chat_history.append({"role": "user", "content": user_answer})

                feedback = pipeline.process_answer(current_question, user_answer)
                with st.expander("Feedback:"):
                    with st.chat_message("assistant"):
                        st.markdown(feedback)
                    st.session_state.chat_history.append({"role": "assistant", "content": feedback})

                follow_up_question = pipeline.generate_follow_up_question(current_question, user_answer)
                with st.chat_message("assistant"):
                    st.markdown(f"{follow_up_question}")
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": f"**Follow-Up Question:** {follow_up_question}"})

                st.session_state.waiting_for_follow_up = True

        else:
            follow_up_answer = st.chat_input("Your answer to the follow-up question")

            if follow_up_answer:
                with st.chat_message("user"):
                    st.markdown(follow_up_answer)
                st.session_state.chat_history.append({"role": "user", "content": follow_up_answer})

                st.session_state.current_question_index += 1
                st.session_state.waiting_for_follow_up = False

    if st.session_state.current_question_index >= len(questions):
        st.session_state.interview_completed = True

    if getattr(st.session_state, 'interview_completed', False):
        with st.chat_message("assistant"):
            overall_feedback = pipeline.generate_overall_feedback(st.session_state.chat_history)
            st.markdown(overall_feedback)
        st.button("Start New Interview", on_click=reset_interview)


def reset_interview():
    st.session_state.current_question_index = 0
    st.session_state.interview_completed = False
    st.session_state.chat_history = []
    st.session_state.waiting_for_follow_up = False