import os
import re
from g4f.client import Client
from g4f.Provider import MetaAI, DDG, Pizzagpt
import g4f
import json
from ai71 import AI71
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()


class RealTimePipeline:
    def __init__(self):
        self.client = AI71(api_key=os.getenv("AI71_API_KEY"))
        self.question_cache = {}
        self.user_metrics = {}

    def generate_text(self, prompt):
        try:
            response = self.client.chat.completions.create(
                    model="tiiuae/falcon-11b",
                    messages=[
                        {"role": "user", "content": prompt},
                    ],
            )
            response = response.choices[0].message.content.strip()
            print(response)
            return response
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return ""

    # def generate_text(self, prompt):
    #     try:
    #         response = self.client.chat.completions.create(
    #             model=g4f.models.gpt_35_turbo,
    #             messages=[{"role": "user", "content": prompt}],
    #             provider=DDG
    #         )
    #         response = response.choices[0].message.content.strip()
    #         print(response)
    #         return response
    #     except Exception as e:
    #         st.error(f"Error generating response: {str(e)}")
    #         return "I'm sorry, I couldn't generate a response at this time."

    def fetch_questions(self, interview_type, job_position=None):
        cache_key = f"{interview_type}_{job_position}" if job_position else interview_type
        if cache_key not in self.question_cache:
            prompt = self.get_question_prompt(interview_type, job_position)
            response = self.generate_text(prompt)

            try:
                questions = json.loads(response)
            except json.JSONDecodeError:
                questions = self.extract_questions_from_text(response)

            questions = [
                {
                    "question": q.get("question", ""),
                    "difficulty": int(q.get("difficulty", 3)),
                    "type": interview_type,
                    "options": q.get("options", []) if interview_type == "Technical" else []
                }
                for q in questions
                if "question" in q
            ]

            self.question_cache[cache_key] = sorted(questions, key=lambda x: x['difficulty'])

        return self.question_cache[cache_key]

    def get_question_prompt(self, interview_type, job_position=None):
        if interview_type == "General":
            return "Generate a list of 20 general interview questions, ranging from easy to hard. For each question, provide the question text and a difficulty level from 1 (easiest) to 5 (hardest). Format your response as a JSON array of objects."
        elif interview_type == "Technical":
            if job_position:
                return f"Generate a list of 20 technical interview questions related to the job position '{job_position}', covering software development, data structures, and algorithms. Include a mix of conceptual questions and coding problems. For each question, provide the question text, a difficulty level from 1 (easiest) to 5 (hardest), and 4 multiple-choice options. Format your response as a JSON array of objects, where each object has 'question', 'difficulty', and 'options' fields."

    def process_answer(self, question, answer):
        prompt = self.get_feedback_prompt(question, answer)
        return self.generate_text(prompt)

    def get_feedback_prompt(self, question, answer):
        if question['type'] == "General":
            return f"Provide constructive feedback for this {question['difficulty']}-level general interview question: '{question['question']}' and the given answer: '{answer}'. Include strengths, areas for improvement, and suggest a way to enhance the answer in shorter form. Consider the following: clarity, relevance"
        elif question['type'] == "Technical":
            return f"Evaluate this {question['difficulty']}-level technical answer to the question: '{question['question']}'. Answer given: '{answer}'. {question['options']} Provide the correct option(s) and explain why and how you would improve the answer. Consider the following: technical accuracy, problem-solving approach, and code quality (if applicable) in most short explanation."

    def generate_overall_feedback(self, chat_history):
        if not chat_history:
            return "No chat history available for feedback."

        interview_type_from_history = chat_history[0]['content'].split()[0] if chat_history else "Unknown"
        prompt = f"Provide an overall assessment of this {interview_type_from_history} interview, including strengths, areas for improvement, and tips for future interviews. Chat history:\n"
        for message in chat_history:
            prompt += f"{message['role'].capitalize()}: {message['content']}\n\n"
        return self.generate_text(prompt)

    def extract_questions_from_text(self, text):
        pattern = r'"question"\s*:\s*"([^"]*)"\s*,\s*"difficulty"\s*:\s*(\d+)(?:,\s*"options"\s*:\s*(\[[^\]]*\]))?'
        matches = re.findall(pattern, text)

        questions = []
        for match in matches:
            question = {
                "question": match[0],
                "difficulty": int(match[1])
            }
            if match[2]:
                try:
                    question["options"] = json.loads(match[2])
                except json.JSONDecodeError:
                    question["options"] = []
            questions.append(question)

        return questions

    def update_metrics(self, username, question_type, feedback):
        if username not in self.user_metrics:
            self.user_metrics[username] = {'general': 0, 'technical': 0}

        score = 1 if "excellent" in feedback.lower() or "great" in feedback.lower() else 0.5
        self.user_metrics[username][question_type.lower()] += score

