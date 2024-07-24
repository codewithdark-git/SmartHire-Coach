from g4f.client import Client
import g4f
import streamlit as st
import PyPDF2
import docx

# Initialize the client
def generate_text(prompt):
    client = Client()
    response = client.chat.completions.create(
        model=g4f.models.gpt_4o,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfFileReader(file)
    text = ""
    for page_num in range(pdf_reader.getNumPages()):
        text += pdf_reader.getPage(page_num).extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

st.title('AI-Powered Job Interview Coach')

# Interview Questions
interview_questions = [
    "Tell me about yourself.",
    "Why do you want to work here?",
    "What are your strengths and weaknesses?",
    "Where do you see yourself in 5 years?",
    "Describe a challenging situation you faced and how you dealt with it."
]

st.header("Mock Interview")
question = st.selectbox("Select a question to answer:", interview_questions)
answer = st.text_area("Your Answer:")

if st.button("Get Feedback"):
    feedback_prompt = f"Provide feedback on this interview answer: '{answer}'"
    feedback = generate_text(feedback_prompt)
    st.text_area("Feedback", feedback)

st.header("Resume Review")
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX):")

if uploaded_file is not None:
    file_type = uploaded_file.type
    if file_type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload a PDF or DOCX file.")
        resume_text = None

    if resume_text:
        st.write("Parsed Resume Data:", resume_text)

        review_prompt = f"Provide suggestions to improve this resume: {resume_text}"
        resume_review = generate_text(review_prompt)
        st.text_area("Resume Review", resume_review)

st.header("Job Search Assistance")

if st.button("Get Job Search Tips"):
    tips_prompt = "Provide some tips for job searching."
    job_search_tips = generate_text(tips_prompt)
    st.text_area("Job Search Tips", job_search_tips)
