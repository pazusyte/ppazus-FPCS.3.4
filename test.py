import random
from datetime import datetime
from constants import ALL_RESULTS
from utils import get_questions, count_questions
from data import Statistics

class EnterTestMode:
    def __init__(self):
        self.question_count = self.get_question_count()
        self.print_questions = PrintQuestions()
        self.count_score = CountScore()
        self.save_results = SaveResults()
    
    def get_question_count(self):
        self.all_questions = count_questions()         
        while True:
            try:
                user_input = input("Enter how many questions do you want: ")
                if user_input.isnumeric():
                    user_input = int(user_input)
                    if 1 <= user_input <= self.all_questions:
                        return user_input
                    else:
                        print(f"There aren't that many questions available. Please enter a valid number.")
                else:
                    print("Please enter a valid number.")
            except ValueError:
                print("Please enter a valid number.")

    def start_test_mode(self):
        selected_questions = self.print_questions.select_random_questions(self.question_count)
        user_answers = self.print_questions.get_user_answers(selected_questions)
        score_results = self.count_score.calculate_score(selected_questions, user_answers)
        self.count_score.display_score(score_results)
        self.save_results.save_results(score_results)

class PrintQuestions:
    def __init__(self):
        self.get_questions = get_questions()

    def select_random_questions(self, num_questions):
        eligible_questions = [question for question in self.get_questions if question["Status"] != "D"]

        if len(eligible_questions) < num_questions:
            raise ValueError("Not enough eligible questions available.")

        selected_questions = random.sample(eligible_questions, num_questions)
        return selected_questions

    def get_user_answers(self, selected_questions):
        user_answers = {}
        for question in selected_questions:
            question_text = question.get("Question")
            options = question.get("Options", "")
            
            print(f"{question_text}")
            
            if options:
                options_list = options.split(';')
                for option in options_list:
                    print(option.strip())

            user_answer = input("Your answer: ").strip()
            question_id = question.get("Question ID")
            user_answers[question_id] = user_answer
        return user_answers

class CountScore: 
    def __init__(self):
        self.statistics = Statistics()

    def calculate_score(self, selected_questions, user_answers):
        score_results = {"total_questions": len(selected_questions), "correct_answers": 0, "results": {}}

        for question in selected_questions:
            question_id = question.get("Question ID")
            self.statistics.increment_show_count(question_id) 
            correct_answer = question.get("Answer")

            if correct_answer is not None:
                user_answer = user_answers.get(question_id, "").strip()
                correct_answer = correct_answer.strip()

                is_correct = user_answer.casefold() == correct_answer.casefold()
                score_results["results"][question_id] = {"correct": is_correct, "user_answer": user_answer}

                if is_correct:
                    score_results["correct_answers"] += 1
                    self.statistics.increment_correct_count(question_id) 
        self.statistics.save_statistics()
        return score_results

    @classmethod   
    def display_score(cls, score_results):
        print(f"Score: {score_results['correct_answers']} / {score_results['total_questions']}")


class SaveResults:
    def save_results(self, score_results):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(ALL_RESULTS, "a") as file:
            file.write(f"\n=== Test Results ===\n")
            file.write(f"Date and Time: {current_time}\n")
            file.write(f"Score: {score_results['correct_answers']} / {score_results['total_questions']}\n")

            for question_id, result in score_results["results"].items():
                correct_indicator = 'Y' if result["correct"] else 'N'

                file.write(f"\nQuestion ID: {question_id}\n")
                file.write(f"User Answer: {result['user_answer']}\n")
                file.write(f"Correct: {correct_indicator}\n")
