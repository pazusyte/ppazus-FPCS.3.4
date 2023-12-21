import csv
from constants import ALL_QUESTIONS

def get_questions():
    all_questions = []

    try:
        with open(ALL_QUESTIONS, "r") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                question_id = row["Question ID"]
                question_text = row["Question"]
                options = row["Options"]
                answer = row["Answer"]
                status = row["Status"]

                question_entry = {
                    "Question ID": question_id,
                    "Question": question_text,
                }

                if options:
                    question_entry["Options"] = options

                question_entry["Answer"] = answer
                question_entry["Status"] = status

                all_questions.append(question_entry)
    except FileNotFoundError:
        pass

    return all_questions

def count_questions():
    with open(ALL_QUESTIONS, "r", newline="") as file:
        reader = csv.DictReader(file)
        question_count = sum(1 for row in reader if row["Status"] == "E")
        question_count = int(question_count)
        return question_count
