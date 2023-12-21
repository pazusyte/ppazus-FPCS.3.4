import pytest
from unittest.mock import patch
from utils import get_questions
from data import Statistics

all_questions = get_questions()

@pytest.fixture
def statistics_instance():
    return Statistics()

def test_increment_show_count(statistics_instance):
    question_id = "1"
    assert question_id not in statistics_instance.show_count

    statistics_instance.increment_show_count(question_id)
    
    assert question_id in statistics_instance.show_count
    assert statistics_instance.show_count[question_id] == 1

def test_increment_correct_count(statistics_instance):
    question_id = "2"
    assert question_id not in statistics_instance.correct_count

    statistics_instance.increment_correct_count(question_id)
    
    assert question_id in statistics_instance.correct_count
    assert statistics_instance.correct_count[question_id] == 1




