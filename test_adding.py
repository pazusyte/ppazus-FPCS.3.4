import pytest
from unittest.mock import patch
from adding import QuestionManager, AddQuestion
from constants import ALL_QUESTIONS
import csv
import io
import shutil

@pytest.fixture
def clear_question_file():
    shutil.copyfile(ALL_QUESTIONS, f"{ALL_QUESTIONS}.bak")

    with open(ALL_QUESTIONS, "a", newline="") as file:
        pass

def test_add_question_freeform(clear_question_file, monkeypatch):
    user_input = ["Test freeform question", "2", "Freeform Answer"]
    user_input_index = 0

    def mock_input(_):
        nonlocal user_input_index
        result = user_input[user_input_index]
        user_input_index += 1
        return result

    monkeypatch.setattr("builtins.input", mock_input)

    add_question_instance = AddQuestion()
    add_question_instance.add_question()

    with open(ALL_QUESTIONS, "r", newline="") as file:
        file.seek(0)
        reader = csv.DictReader(file)
        added_question = next(reader)

    assert added_question["Question ID"] == "Q0001"
    assert added_question["Question"] == "Test freeform question"
    assert added_question["Answer"] == "Freeform Answer"
    assert added_question["Status"] == "E"

    shutil.move(f"{ALL_QUESTIONS}.bak", ALL_QUESTIONS)
