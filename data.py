from utils import get_questions
from constants import STATISTICS
import csv
from tabulate import tabulate

all_questions = get_questions()

class Statistics:
    def __init__(self):
        self._show_count = {}
        self._correct_count = {}
        self._correct_percentage = {}
        self.load_previous_counts()

    @property
    def show_count(self):
        return self._show_count

    @property
    def correct_count(self):
        return self._correct_count

    def increment_show_count(self, question_id):
        self._show_count[question_id] = self._show_count.get(question_id, 0) + 1

    def increment_correct_count(self, question_id):
        self._correct_count[question_id] = self._correct_count.get(question_id, 0) + 1

    def load_previous_counts(self):
        load_previous_counts_from_file(STATISTICS, self._show_count, self._correct_count, self._correct_percentage)

    def save_statistics(self):
        save_statistics_to_file(STATISTICS, all_questions, self._show_count, self._correct_count, self._correct_percentage)
    
    def print_statistics(self):
        load_previous_counts_from_file(STATISTICS, self._show_count, self._correct_count, self._correct_percentage)

        data = []
        for question_id in self._show_count:
            shown_count = self._show_count.get(question_id, 0)
            correct_percentage_value = self._correct_percentage.get(question_id, 0)

            question = next((q for q in all_questions if q.get("Question ID") == question_id), None)
            if question:
                data.append({
                    "Question ID": question_id,
                    "Question": question.get("Question", ""),
                    "Options": question.get("Options", ""),
                    "Status": question.get("Status", ""),
                    "Show Count": shown_count,
                    "Correct Percentage": correct_percentage_value,
                })

        headers = ["Question ID", "Question", "Options", "Status", "Show Count", "Correct Percentage"]
        print(tabulate(data, headers="keys", tablefmt="pretty"))

def load_previous_counts_from_file(filename, show_count, correct_count, correct_percentage):
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                question_id = row["Question ID"]
                shown_count = int(row["Show Count"])
                correct_count_value = int(row["Correct Count"])
                correct_percentage_value = float(row["Correct Percentage"])

                show_count[question_id] = shown_count
                correct_count[question_id] = correct_count_value
                correct_percentage[question_id] = correct_percentage_value

    except FileNotFoundError:
        pass

def save_statistics_to_file(filename, questions, show_count, correct_count, correct_percentage):
    with open(filename, "w", newline="") as file:
        fieldnames = ["Question ID", "Question", "Options", "Status", "Show Count", "Correct Count", "Correct Percentage"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for question in questions:
            question_id = question.get("Question ID")
            shown_count = show_count.get(question_id, 0)
            correct_count_value = correct_count.get(question_id, 0)
            if shown_count > 0:
                correct_percentage_value = round((correct_count_value / shown_count) * 100, 2)
            else:
                correct_percentage_value = 0

            writer.writerow({
                "Question ID": question_id,
                "Question": question.get("Question", ""),
                "Options": question.get("Options", ""),
                "Status": question.get("Status", ""),
                "Show Count": shown_count,
                "Correct Count": correct_count_value,
                "Correct Percentage": correct_percentage_value,
            })


