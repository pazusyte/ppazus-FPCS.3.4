from utils import get_questions
from constants import ALL_QUESTIONS
import csv

class StatusManager:
    def __init__(self):
        self.all_questions = get_questions()
        self.question_found = False

    def replace_status(self, question_entry):
        current_status = question_entry["Status"]

        if current_status == "E":
            question_entry["Status"] = "D"
        else:
            question_entry["Status"] = "E"

    def find_question_by_id(self, question_id):
        for question_entry in self.all_questions:
            if question_entry["Question ID"] == question_id:
                return question_entry
        return None

    def display_question(self, question_entry):
        print("Question ID:", question_entry["Question ID"])
        print("Question:", question_entry["Question"])
        print("Answer:", question_entry["Answer"])

    def change_status(self, question_id):
        question_entry = self.find_question_by_id(question_id)
        if question_entry:
            self.display_question(question_entry)
            while True:
                confirm = input(f"Do you really want to change the status of question {question_id} (y/n)? ")
                if confirm.casefold() == "y":
                    self.replace_status(question_entry)
                    print(f"Status of question {question_id} changed.")
                    break
                elif confirm.casefold() == "n":
                    print("No changes were made.")
                    break
                else:
                    continue
        else:
            print("Question ID not found.")

    def save_questions_to_file(self):
        with open(ALL_QUESTIONS, "w", newline="") as file:
            fieldnames = ["Question ID", "Question", "Options", "Answer", "Status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.all_questions)
