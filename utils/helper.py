import streamlit as st
import docx
import PyPDF2
from utils.real_time_pipeline import RealTimePipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import re


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
