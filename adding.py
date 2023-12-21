import random
import string
import os
import csv
from constants import ALL_QUESTIONS

class QuestionManager:
    @classmethod
    def generate_question_id(cls):
        if not os.path.isfile(ALL_QUESTIONS):
            next_id = 1
        else:
            with open(ALL_QUESTIONS, "r", newline="") as file:
                reader = csv.DictReader(file)
                question_ids = [int(row["Question ID"][1:]) for row in reader if row["Question ID"][1:].isdigit()]
                next_id = max(question_ids, default=0) + 1
        return f"Q{next_id:04d}"
    
    @staticmethod
    def add_question(question_type, question_text, answer, options=None):
        question_id = QuestionManager.generate_question_id()

        question = {
            "id": question_id,
            "type": question_type,
            "question": question_text,
            "answer": answer,
            "options": options
        }

        print(f"Question with ID {question_id} added successfully.")
        print_to_file(question)

def print_to_file(question):
    file_exists = os.path.isfile(ALL_QUESTIONS)

    with open(ALL_QUESTIONS, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Question ID", "Question", "Options", "Answer", "Status"])

        if not file_exists:
            writer.writeheader()

        if question['type'] == "2":
            writer.writerow({"Question ID": question['id'], "Question": question['question'], "Options": "", "Answer": question['answer']['answer'], "Status": "E"})
        elif question['type'] == "1":
            options_string = ";".join([f"{option['label']}: {option['answer']}" for option in question['options']])
            correct_answer_label = next((option['label'] for option in question['options'] if option['answer'] == question['answer']), None)
            writer.writerow({"Question ID": question['id'], "Question": question['question'], "Options": options_string, "Answer": correct_answer_label, "Status": "E"})

class AddQuestion:
    def __init__(self):
        self.question_manager = QuestionManager()

    def add_question(self):
        question_text = input("Enter question: ")
        question_type = input("Enter question type: 1. Quiz 2. Free-form): ").lower().strip()

        options = None

        if question_type == "1":
            answer_dict = get_quiz_answer()
            answer = answer_dict["answer"]
            options = answer_dict["options"]

        elif question_type == "2":
            answer = get_freeform_answer()
        else:
            print("Invalid question type. Please enter 1 for Quiz or 2 for Free-form.")
        
        self.question_manager.add_question(question_type, question_text, answer, options=options)

def get_freeform_answer():
        return {"answer": input("Enter answer: ")}
    
def get_quiz_answer():
    correct_answer = input("Enter the correct answer: ")

    options_input = input("Enter incorrect options (comma-separated): ")
    incorrect_options = [option.strip() for option in options_input.split(',')]

    all_options = [{"answer": correct_answer, "label": ""}] + [{"answer": option, "label": ""} for option in incorrect_options]

    random.shuffle(all_options)

    alphabet = list(string.ascii_uppercase)
    options_with_labels = [{"label": letter, "answer": option["answer"]} for letter, option in zip(sorted(alphabet), all_options)]

    return {"answer": correct_answer, "options": options_with_labels}