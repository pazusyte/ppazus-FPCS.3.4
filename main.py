from adding import AddQuestion
from test import EnterTestMode
from practice import PracticeMode
from status import StatusManager
from data import Statistics
import os
import sys
from constants import ALL_QUESTIONS
from utils import count_questions, get_questions

modes = ["1. Adding questions", "2. Statistics viewing", "3. Disable/enable questions", "4. Practice mode", "5. Test mode"]

def main():
    while True:
        try:
            for mode in modes:
                print(mode)
            mode_input = input("Choose the mode from the above list: ").strip()

            if mode_input == "1":
                add_question_mode()
            elif mode_input == "5":
                if has_enough_questions():
                    test_mode()
            elif mode_input == "4":
                if has_enough_questions():
                    practice_mode()
            elif mode_input == "3":
                status_mode()
            elif mode_input == "2":
                statistics_mode()
            else:
                print("Please choose a valid mode")

            while True:
                switch_mode = input("Do you want to switch the mode? (y/n): ").strip().lower()
                if switch_mode == "y":
                    break
                elif switch_mode == "n":
                    sys.exit()

        except EOFError:
            sys.exit()

def add_question_mode():
    while True:
        add_question_instance = AddQuestion()
        add_question_instance.add_question()

        add_more_questions = input("Do you want to add more questions? (y/n): ").strip().lower()

        if add_more_questions != "y":
            break

def test_mode():
    while True:
        try:
            test_mode_instance = EnterTestMode()
            test_mode_instance.start_test_mode()

            repeat_test = input("Do you want to do another test? (y/n): ").strip().lower()

            if repeat_test != "y":
                break
        except ValueError:
            break

def practice_mode():
    practice_mode_instance = PracticeMode()
    practice_mode_instance.start_practice_mode()

def has_enough_questions():
    if not os.path.isfile(ALL_QUESTIONS):
        return False
    
    question_count = count_questions()

    if question_count >= 5:
        print(f"There are {question_count} questions available.")
        return True
    else:
        print("You need at least 5 active questions to enter this mode.")
        return False

def status_mode():
    while True:
        try:
            question_manager = StatusManager()
            question_actioned = input("Input the Question ID of the question you want to disable/enable: ")
            question_manager.change_status(question_actioned)
            question_manager.save_questions_to_file()
            repeat_change = input("Do you want to change the status of another question? (y/n): ").strip().lower()

            if repeat_change != "y":
                break
        except ValueError:
            break

def statistics_mode():
    statistics_instance = Statistics()
    statistics_instance.print_statistics()

if __name__ == "__main__":
    main()


#Link to the Part 3 repository: https://github.com/pazusyte/Turing-1.3.3.git