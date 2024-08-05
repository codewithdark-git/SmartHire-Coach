import streamlit as st
import docx
import PyPDF2
from utils.real_time_pipeline import RealTimePipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import re

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

pipeline = RealTimePipeline()


@st.cache_data
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    return " ".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())


@st.cache_data
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text)


@st.cache_data
def analyze_resume(resume_text):
    skills = extract_skills(resume_text)
    experience_summary = summarize_experience(resume_text)
    education = extract_education(resume_text)
    return skills, experience_summary, education


def extract_skills(text):
    common_skills = ["Python", "Java", "C++", "JavaScript", "React", "Node.js", "SQL", "Machine Learning",
                     "Data Analysis", "Project Management"]
    found_skills = [skill for skill in common_skills if skill.lower() in text.lower()]

    skill_pattern = r'\b(?:proficient in|experienced with|skilled in|knowledge of)\s+([\w\s]+)'
    additional_skills = re.findall(skill_pattern, text, re.IGNORECASE)

    return list(set(found_skills + additional_skills))


def summarize_experience(text):
    experience_keywords = ["experience", "work", "job", "position", "role"]
    experience_sentences = [sent for sent in nltk.sent_tokenize(text)
                            if any(keyword in sent.lower() for keyword in experience_keywords)]
    return " ".join(experience_sentences[:3])


def extract_education(text):
    education_keywords = ["education", "university", "college", "degree", "bachelor", "master", "phd"]
    education_sentences = [sent for sent in nltk.sent_tokenize(text)
                           if any(keyword in sent.lower() for keyword in education_keywords)]
    return " ".join(education_sentences)


def generate_prompt(skills, experience_summary, education):
    return f"""Based on the following resume analysis, provide improvement suggestions and job recommendations:

Skills: {', '.join(skills)}
Experience Summary: {experience_summary}
Education: {education}

Please provide:
1. Three specific improvements the candidate could make to their resume.
2. Three job roles or positions that would be suitable for this candidate based on their skills and experience.

Respond in the following format:
Improvements:
1. [Improvement 1]
2. [Improvement 2]
3. [Improvement 3]

Job Suggestions:
1. [Job Role 1]
2. [Job Role 2]
3. [Job Role 3]

"""


def calculate_resume_score(resume_text, skills, education):
    score = 0
    score += 30 if len(skills) >= 5 else (20 if len(skills) >= 3 else 10)
    score += 20 if education else 0
    score += 30 if len(resume_text.split()) > 300 else (20 if len(resume_text.split()) > 200 else 10)
    return min(score, 100)


def parse_response(response):
    try:
        improvements, job_suggestions = response.split("Job Suggestions:")
        improvements = improvements.split("Improvements:")[1].strip().split("\n")
        job_suggestions = job_suggestions.strip().split("\n")
        return [imp.strip()[3:] for imp in improvements if imp.strip()], [job.strip()[3:] for job in job_suggestions if
                                                                          job.strip()]
    except Exception:
        raise ValueError("Unexpected response format")


def main():
    st.set_page_config(page_title="Advanced Resume Analyzer", page_icon="📄", layout="wide")

    st.title("📄 Advanced Resume Analyzer")
    st.write("Upload your resume and get personalized insights and recommendations!")

    uploaded_file = st.file_uploader("📎 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

    if uploaded_file is not None:
        progress_bar = st.progress(0)
        progress_text = st.empty()

        progress_text.text("Analyzing your resume... This may take a moment.")
        try:
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = extract_text_from_docx(uploaded_file)
            else:
                st.error("❌ Unsupported file format. Please upload a PDF or DOCX file.")
                return

            progress_bar.progress(25)
            progress_text.text("Extracting information from the resume...")
            skills, experience_summary, education = analyze_resume(resume_text)
            progress_bar.progress(50)

            progress_text.text("Generating insights and recommendations...")
            prompt = generate_prompt(skills, experience_summary, education)

            try:
                response = pipeline.generate_text(prompt)
                improvements, job_suggestions = parse_response(response)
            except Exception as e:
                st.error(f"❌ Error in generating improvements and job suggestions: {str(e)}")
                improvements = ["Unable to generate improvements at this time."]
                job_suggestions = ["Unable to generate job suggestions at this time."]

            resume_score = calculate_resume_score(resume_text, skills, education)
            progress_bar.progress(75)

            progress_text.text("Finalizing the analysis...")
            st.success("✅ Resume analysis complete!")

            st.subheader("📊 Resume Score")
            st.progress(resume_score / 100)
            st.write(f"Your resume scored {resume_score}/100")

            st.subheader("🚀 Improvement Suggestions")
            for i, imp in enumerate(improvements, 1):
                st.write(f"{i}. {imp}")

            st.subheader("🔍 Extracted Skills")
            skills = f""" {resume_text} this is resume text and we want to Extract skills from the resume using the following pattern (case-insensitive):
                        proficient in " or " experienced with " or " skilled in " or " knowledge of " followed
                        by a comma-separated list of skills. Example: 'Experienced with Python, Java, SQL,
                        JavaScript, React, Node.js, and Machine Learning.' """
            res = pipeline.generate_text(skills)
            st.write(res)

            st.subheader("💼 Potential Job Matches")
            for i, job in enumerate(job_suggestions, 1):
                st.write(f"{i}. {job}")

            st.subheader("📚 Education")
            edu_prompt = f"""Summarize the education details from: {education}
            Format the response as: "Degree, Institution, Years of Study"
            Example: "Bachelor of Science in Computer Science, University of California, Los Angeles, 2015-2020"
            If specific details are missing, use placeholder text."""
            edu_response = pipeline.generate_text(edu_prompt)
            st.write(edu_response)

            st.subheader("💡 Experience Summary")
            exp_prompt = f"""Summarize the work experience from: {experience_summary}
            Format the response as: "Job Title, Company Name, Location, Years of Experience, Brief Description"
            Example: "Software Engineer, Google, Mountain View, 3 years, Developed web applications using Python and Django"
            If specific details are missing, use placeholder text. Limit to 2-3 most recent or relevant positions."""
            exp_response = pipeline.generate_text(exp_prompt)
            st.write(exp_response)

            progress_bar.progress(100)
            progress_text.text("Analysis complete.")

        except Exception as e:
            st.error(f"❌ An error occurred while processing the resume: {str(e)}")
            st.write("Please try uploading your resume again or contact support if the issue persists.")


if __name__ == "__main__":
    main()
