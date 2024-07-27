import json
import re
import streamlit as st
import g4f
from g4f.client import Client


class RealTimePipeline:
    def __init__(self):
        self.client = Client()
        self.question_cache = {}
        self.user_metrics = {}

    def generate_text(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=g4f.models.gpt_4o,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return "I'm sorry, I couldn't generate a response at this time."

    def fetch_questions(self, interview_type):
        if interview_type not in self.question_cache:
            prompt = self.get_question_prompt(interview_type)
            response = self.generate_text(prompt)

            try:
                questions = json.loads(response)
            except json.JSONDecodeError:
                questions = self.extract_questions_from_text(response)

            questions = [
                {
                    "question": q.get("question", ""),
                    "difficulty": int(q.get("difficulty", 3)),
                    "type": interview_type
                }
                for q in questions
                if "question" in q
            ]

            self.question_cache[interview_type] = sorted(questions, key=lambda x: x['difficulty'])

        return self.question_cache[interview_type]

    def get_question_prompt(self, interview_type):
        if interview_type == "General":
            return "Generate a list of 10 general interview questions, ranging from easy to hard. For each question, provide the question text and a difficulty level from 1 (easiest) to 5 (hardest). Format your response as a JSON array of objects."
        elif interview_type == "Technical":
            return "Generate a list of 10 technical interview questions related to software development, data structures, and algorithms. Include a mix of conceptual questions and coding problems. For each question, provide the question text and a difficulty level from 1 (easiest) to 5 (hardest). Format your response as a JSON array of objects."
        elif interview_type == "Behavioral":
            return "Generate a list of 10 behavioral interview questions that assess a candidate's soft skills, problem-solving abilities, and past experiences. For each question, provide the question text and a difficulty level from 1 (easiest) to 5 (hardest). Format your response as a JSON array of objects."

    def process_answer(self, question, answer):
        prompt = self.get_feedback_prompt(question, answer)
        return self.generate_text(prompt)

    def get_feedback_prompt(self, question, answer):
        if question['type'] == "General":
            return f"Provide constructive feedback for this {question['difficulty']}-level general interview question: '{question['question']}' and the given answer: '{answer}'. Include strengths,the correct version of answer areas for improvement, and suggest a way to enhance the answer."
        elif question['type'] == "Technical":
            return f"Evaluate this {question['difficulty']}-level technical answer to the question: '{question['question']}'. Answer given: '{answer}'. Assess technical accuracy, problem-solving approach, and code quality (if applicable). Provide specific technical improvements or alternative solutions if needed."
        elif question['type'] == "Behavioral":
            return f"Analyze this {question['difficulty']}-level response to the behavioral question: '{question['question']}'. Answer: '{answer}'. Evaluate the use of the STAR method (Situation, Task, Action, Result), specificity of examples, and demonstration of relevant skills. Suggest ways to strengthen the response."

    def generate_follow_up_question(self, question, answer):
        prompt = self.get_follow_up_prompt(question, answer)
        return self.generate_text(prompt)

    def get_follow_up_prompt(self, question, answer):
        if question['type'] == "General":
            return f"Based on the general interview question '{question['question']}' and the given answer: '{answer}', generate a relevant follow-up question to delve deeper into the candidate's knowledge or experience."
        elif question['type'] == "Technical":
            return f"Given the technical question '{question['question']}' and the response: '{answer}', formulate a follow-up question that either probes deeper into the technical concept, asks for optimization of the solution, or explores related technical knowledge."
        elif question['type'] == "Behavioral":
            return f"Considering the behavioral question '{question['question']}' and the provided answer: '{answer}', create a follow-up question that encourages the candidate to elaborate on their actions, decision-making process, or the outcomes of the situation they described."

    def generate_overall_feedback(self, chat_history):
        interview_type = chat_history[0]['content'].split()[0]  # Extract interview type from first message
        prompt = f"Provide an overall assessment of this {interview_type} interview, including strengths, areas for improvement, and tips for future interviews. Chat history:\n"
        for message in chat_history:
            prompt += f"{message['role'].capitalize()}: {message['content']}\n\n"
        return self.generate_text(prompt)

    def extract_questions_from_text(self, text):
        pattern = r'"question"\s*:\s*"([^"]*)"\s*,\s*"difficulty"\s*:\s*(\d+)'
        matches = re.findall(pattern, text)

        questions = [
            {"question": match[0], "difficulty": int(match[1])}
            for match in matches
        ]

        return questions

    def update_metrics(self, username, question_type, feedback):
        if username not in self.user_metrics:
            self.user_metrics[username] = {'general': 0, 'technical': 0, 'behavioral': 0}

        score = 1 if "excellent" in feedback.lower() or "great" in feedback.lower() else 0.5
        self.user_metrics[username][question_type.lower()] += score