import random
from test import PrintQuestions, CountScore
from utils import get_questions
from data import Statistics
from constants import WEIGHTS

class PracticeMode:
    def __init__(self):
        self.print_questions_instance = PrintQuestions()
        self.count_score = CountScore()
        self.questions = get_questions()
        self.weights = self.load_weights() or [(question["Question ID"], 1.0) for question in self.questions]
        self.statistics = Statistics()

    def start_practice_mode(self):
        while True:
            try:
                self.sync_weights_with_questions()

                weights_list = [weight for _, weight in self.weights]

                selected_index = random.choices(range(len(self.questions)), weights_list)[0]
                selected_question = self.questions[selected_index]
                question_id = selected_question["Question ID"]
                self.statistics.increment_show_count(question_id)
                print(f"Question: {selected_question['Question']}")

                if "Options" in selected_question:
                    options = selected_question["Options"]
                    if options:
                        options_list = options.split(';')
                        for option in options_list:
                            print(option.strip())

                user_answer = input("Your answer: ").strip()

                is_correct = user_answer.casefold() == selected_question["Answer"].casefold()
                if is_correct:
                    self.statistics.increment_correct_count(question_id)
                    current_weight = self.weights[selected_index][1]
                    new_weight = current_weight / 2
                    self.weights[selected_index] = (question_id, new_weight)
                    print("Correct!")
                else:
                    current_weight = self.weights[selected_index][1]
                    new_weight = current_weight * 2
                    self.weights[selected_index] = (question_id, new_weight)
                    print("Incorrect")

                total_weight = sum(weight for _, weight in self.weights)
                self.weights = [(question_id, weight / total_weight) for question_id, weight in self.weights]
                self.statistics.save_statistics()
                self.save_weights()

            except EOFError:
                print("")
                break

    def save_weights(self):
        with open(WEIGHTS, "w") as file:
            for question in self.questions:
                question_id = question["Question ID"]
                weight = next((w for q_id, w in self.weights if q_id == question_id), 1.0)
                file.write(f"{question_id} {weight}\n")


    def load_weights(self):
        try:
            with open(WEIGHTS, "r") as file:
                return [(line.split()[0], float(line.split()[1])) for line in file]
        except FileNotFoundError:
            return [(question["Question ID"], 1.0) for question in self.questions]
    
    def sync_weights_with_questions(self):
        for question in self.questions:
            question_id = question["Question ID"]
            if not any(q_id == question_id for q_id, _ in self.weights):
                self.weights.append((question_id, 1.0))

