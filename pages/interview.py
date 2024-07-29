import streamlit as st

def interview_chatbot(pipeline, interview_type):
    st.header(f"{interview_type} Interview Practice")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    for idx, message in enumerate(st.session_state.chat_history):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0

    if 'waiting_for_follow_up' not in st.session_state:
        st.session_state.waiting_for_follow_up = False

    if interview_type == "Technical" and 'job_position' not in st.session_state:
        st.chat_message("assistant").markdown("Please enter the specific job position you are preparing for interview.")
        job_position = st.chat_input("Your job position", key="job_position_input")
        if job_position:
            st.chat_message("user").markdown(job_position)
            st.session_state.job_position = job_position
            st.experimental_rerun()

    questions = pipeline.fetch_questions(interview_type, st.session_state.get('job_position'))

    if st.session_state.current_question_index < len(questions):
        current_question = questions[st.session_state.current_question_index]

        if not st.session_state.waiting_for_follow_up:
            if not st.session_state.chat_history or st.session_state.chat_history[-1]["role"] != "assistant":
                with st.chat_message("assistant"):
                    st.markdown(current_question['question'])
                st.session_state.chat_history.append({"role": "assistant", "content": current_question['question']})

            user_answer = st.chat_input("Your answer", key=f"user_answer_{st.session_state.current_question_index}")

            if user_answer:
                with st.chat_message("user"):
                    st.markdown(user_answer)
                st.session_state.chat_history.append({"role": "user", "content": user_answer})

                feedback = pipeline.process_answer(current_question, user_answer)

                with st.chat_message("assistant"):
                    st.markdown(feedback)
                st.session_state.chat_history.append({"role": "assistant", "content": feedback})

                follow_up_question = pipeline.generate_follow_up_question(current_question, user_answer)
                with st.chat_message("assistant"):
                    st.markdown(f"**Follow-Up Question:** {follow_up_question}")
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": f"**Follow-Up Question:** {follow_up_question}"})

                st.session_state.waiting_for_follow_up = True
                st.experimental_rerun()

        else:
            follow_up_answer = st.chat_input("Your answer to the follow-up question", key=f"follow_up_{st.session_state.current_question_index}")

            if follow_up_answer:
                with st.chat_message("user"):
                    st.markdown(follow_up_answer)
                st.session_state.chat_history.append({"role": "user", "content": follow_up_answer})

                st.session_state.current_question_index += 1
                st.session_state.waiting_for_follow_up = False
                st.experimental_rerun()

    if st.session_state.current_question_index >= len(questions):
        st.session_state.interview_completed = True

    if getattr(st.session_state, 'interview_completed', False):
        with st.chat_message("assistant"):
            overall_feedback = pipeline.generate_overall_feedback(st.session_state.chat_history)
            st.markdown(overall_feedback)
        if st.button("Start New Interview", key=f"new_interview_{interview_type}"):
            reset_interview()
            st.experimental_rerun()

def reset_interview():
    for key in ['current_question_index', 'interview_completed', 'chat_history', 'waiting_for_follow_up', 'job_position']:
        if key in st.session_state:
            del st.session_state[key]