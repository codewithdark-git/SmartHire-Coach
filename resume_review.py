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
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

def run_resume_review():
    st.title('Resume Review')
    st.write("Upload your resume (PDF or DOCX) for feedback and improvement suggestions.")
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
            st.subheader("Uploaded Resume")
            st.write(resume_text)
            review_prompt = f"Provide suggestions to improve this resume: {resume_text}"
            resume_review = generate_text(review_prompt)
            st.text_area("Resume Review", resume_review, height=150)
