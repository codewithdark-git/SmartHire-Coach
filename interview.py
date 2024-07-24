import streamlit as st
import random
from g4f.client import Client
import g4f

# Initialize the client
def generate_text(prompt):
    try:
        client = Client()
        response = client.chat.completions.create(
            model=g4f.models.gpt_35_turbo,
            messages=[{"role": "user", "content": prompt}],
            provider="DDG"
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating text: {e}")
        return ""

# Generate job-specific questions
def generate_job_specific_questions(job_title):
    prompt = (f"Generate 5 multiple-choice questions for a {job_title} interview. Each question "
              "should have 4 options. Include a mix of technical, theoretical, and practical questions. "
              "Format: Question|Option1|Option2|Option3|Option4|CorrectAnswerNumber|QuestionType")
    response = generate_text(prompt)
    questions = []
    for line in response.split('\n'):
        parts = line.split('|')
        if len(parts) == 7:
            questions.append({
                'question': parts[0],
                'options': parts[1:5],
                'correct_answer': int(parts[5]) - 1,
                'question_type': parts[6]
            })
    return questions

# Generate feedback for general questions
def generate_feedback(question, answer):
    prompt = (f"For the interview question '{question}', the candidate answered: '{answer}'. Provide constructive "
              "feedback on this answer, including strengths and potential areas for improvement. "
              "Keep the feedback concise, around 2-3 sentences.")
    return generate_text(prompt)

# General interview questions
general_interview_questions = [
    "Tell me about yourself.",
    "Why do you want to work here?",
    "What are your strengths and weaknesses?",
    "Where do you see yourself in 5 years?",
    "Describe a challenging situation you faced and how you dealt with it."
]

# Main function to run the mock interview
def run_mock_interview():
    st.title('Mock Interview')
    st.write("Prepare for your interview with our AI-powered mock interview session.")

    if 'step' not in st.session_state:
        initialize_session()

    if st.session_state.step == 'general_questions':
        handle_general_questions()
    elif st.session_state.step == 'job_questions':
        handle_job_questions()
    elif st.session_state.step == 'summary':
        show_summary()

# Initialize session state
def initialize_session():
    st.session_state.step = 'general_questions'
    st.session_state.question_index = 0
    st.session_state.answers = []
    st.session_state.feedbacks = []
    st.session_state.job_title = None
    st.session_state.job_questions = []
    st.session_state.current_job_question = 0
    st.session_state.score = 0

# Handle general questions
def handle_general_questions():
    if st.session_state.question_index < len(general_interview_questions):
        question = general_interview_questions[st.session_state.question_index]
        st.subheader(f"Question {st.session_state.question_index + 1}: {question}")

        answer = st.text_area("Your Answer:", key=f"answer_{st.session_state.question_index}")

        if st.button("Submit Answer", key=f"submit_{st.session_state.question_index}"):
            if answer:
                with st.spinner("Generating feedback..."):
                    feedback = generate_feedback(question, answer)
                st.session_state.answers.append(answer)
                st.session_state.feedbacks.append(feedback)
                st.success("Answer submitted successfully!")
                st.write("Feedback:", feedback)
                st.session_state.question_index += 1
                st.rerun()
            else:
                st.warning("Please provide an answer before submitting.")
    else:
        st.session_state.step = 'job_questions'
        st.rerun()

# Handle job-specific questions
def handle_job_questions():
    if st.session_state.job_title is None:
        st.subheader("Enter Job Title")
        st.session_state.job_title = st.text_input("Enter the job title you're interviewing for:")

        if st.session_state.job_title:
            with st.spinner("Generating job-specific questions..."):
                st.session_state.job_questions = generate_job_specific_questions(st.session_state.job_title)
            st.session_state.current_job_question = 0
            st.rerun()

    if st.session_state.current_job_question < len(st.session_state.job_questions):
        question = st.session_state.job_questions[st.session_state.current_job_question]
        st.subheader(f"Job-Specific Question {st.session_state.current_job_question + 1}: {question['question']}")
        st.write(f"Type: {question['question_type']}")

        user_answer = st.radio("Select your answer:", question['options'], key=f"q_{st.session_state.current_job_question}")

        if st.button("Submit Answer", key=f"submit_job_{st.session_state.current_job_question}"):
            correct_answer = question['options'][question['correct_answer']]
            if user_answer == correct_answer:
                st.success("Correct!")
                st.session_state.score += 1
                feedback = "Great job! Your answer was correct."
            else:
                st.error(f"Incorrect. The correct answer was: {correct_answer}")
                feedback = f"Your answer was incorrect. The correct answer is: {correct_answer}. Consider reviewing this topic."

            st.write("Feedback:", feedback)
            st.session_state.answers.append(user_answer)
            st.session_state.feedbacks.append(feedback)
            st.session_state.current_job_question += 1
            if st.session_state.current_job_question < len(st.session_state.job_questions):
                st.rerun()
            else:
                st.session_state.step = 'summary'
                st.rerun()

# Show interview summary
def show_summary():
    st.subheader("Interview Summary")

    st.write("General Questions:")
    for i, (question, answer, feedback) in enumerate(zip(general_interview_questions,
                                                         st.session_state.answers[:len(general_interview_questions)],
                                                         st.session_state.feedbacks[:len(general_interview_questions)])):
        st.write(f"Question {i + 1}: {question}")
        st.write(f"**Your Answer:** {answer}")
        st.write(f"**Feedback:** {feedback}")
        st.write("---")

    if st.session_state.job_questions:
        st.write("Job-Specific Questions:")
        total_score = len(st.session_state.job_questions)
        st.write(f"Your score on technical questions: {st.session_state.score}/{total_score}")
        for i, (question, answer, feedback) in enumerate(zip(st.session_state.job_questions,
                                                             st.session_state.answers[len(general_interview_questions):],
                                                             st.session_state.feedbacks[len(general_interview_questions):])):
            st.write(f"Question {i + 1} ({question['question_type']}): {question['question']}")
            st.write(f"**Your Answer:** {answer}")
            st.write(f"**Feedback:** {feedback}")
            st.write("---")

    if st.button("Restart Interview"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

if __name__ == '__main__':
    run_mock_interview()
