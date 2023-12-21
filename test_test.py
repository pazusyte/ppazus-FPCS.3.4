import pytest
from unittest.mock import patch, MagicMock
from test import EnterTestMode

@pytest.fixture
def enter_test_mode_instance():
    return EnterTestMode()

def test_start_test_mode(enter_test_mode_instance):
    enter_test_mode_instance.print_questions = MagicMock()
    enter_test_mode_instance.count_score = MagicMock()
    enter_test_mode_instance.save_results = MagicMock()

    selected_questions = [{"Question ID": 1, "Question": "Q1", "Options": "A;B;C", "Status": "A"},
                          {"Question ID": 2, "Question": "Q2", "Options": "A;B;C", "Status": "A"}]
    user_answers = {1: "A", 2: "B"}
    score_results = {"total_questions": 2, "correct_answers": 1, "results": {1: {"correct": True, "user_answer": "A"}}}

    enter_test_mode_instance.print_questions.select_random_questions.return_value = selected_questions
    enter_test_mode_instance.print_questions.get_user_answers.return_value = user_answers
    enter_test_mode_instance.count_score.calculate_score.return_value = score_results

    enter_test_mode_instance.start_test_mode()

    enter_test_mode_instance.print_questions.select_random_questions.assert_called_once_with(2)
    enter_test_mode_instance.print_questions.get_user_answers.assert_called_once_with(selected_questions)
    enter_test_mode_instance.count_score.calculate_score.assert_called_once_with(selected_questions, user_answers)
    enter_test_mode_instance.count_score.display_score.assert_called_once_with(score_results)
    enter_test_mode_instance.save_results.save_results.assert_called_once_with(score_results)
