from typing import List
import streamlit as st
import PyPDF2
# import docx


@st.cache_data

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def read_file(file):
    if file.type == "application/pdf":
        return read_pdf(file)
    # elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
    #     return read_docx(file)
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        return "Unsupported file type"


# def read_docx(file):
#     doc = docx.Document(file)
#     return "\n".join([para.text for para in doc.paragraphs])


def split_text_into_chunks(text, chunk_size=3000):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])
