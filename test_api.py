# Тести для Flask API — Генетичний алгоритм складання розкладу
# Автор: Баранова Анастасія, група АІ-231

import pytest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, InputData, GeneticScheduler

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_health_endpoint(client):
    """GET /health повертає статус ok"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'ok'

def test_calculate_empty_body(client):
    """POST /calculate з порожнім тілом повертає 200"""
    response = client.post('/calculate',
                           data=json.dumps({}),
                           content_type='application/json')
    assert response.status_code == 200


def test_calculate_returns_success(client):
    """Відповідь містить status: success"""
    response = client.post('/calculate',
                           data=json.dumps({}),
                           content_type='application/json')
    data = json.loads(response.data)
    assert data['status'] == 'success'


def test_calculate_has_result_fields(client):
    """Відповідь містить всі обов'язкові поля result"""
    response = client.post('/calculate',
                           data=json.dumps({
                               'max_generations': 5,
                               'pop_size': 10
                           }),
                           content_type='application/json')
    data = json.loads(response.data)
    result = data['result']
    for field in ('conflicts', 'gaps', 'pref_deviation',
                  'final_score', 'iterations_done', 'schedule_size',
                  'schedule_preview'):
        assert field in result, f"Поле '{field}' відсутнє у result"


def test_calculate_custom_params(client):
    """Передані параметри відображаються у полі input"""
    payload = {'teachers_count': 5, 'courses_count': 10,
               'max_generations': 5, 'pop_size': 10}
    response = client.post('/calculate',
                           data=json.dumps(payload),
                           content_type='application/json')
    data = json.loads(response.data)
    assert data['input']['teachers_count'] == 5
    assert data['input']['courses_count'] == 10


def test_calculate_conflicts_non_negative(client):
    """Кількість конфліктів не може бути від'ємною"""
    response = client.post('/calculate',
                           data=json.dumps({
                               'max_generations': 5,
                               'pop_size': 10
                           }),
                           content_type='application/json')
    data = json.loads(response.data)
    assert data['result']['conflicts'] >= 0


def test_calculate_schedule_preview_length(client):
    """schedule_preview містить не більше 5 елементів"""
    response = client.post('/calculate',
                           data=json.dumps({
                               'max_generations': 5,
                               'pop_size': 10
                           }),
                           content_type='application/json')
    data = json.loads(response.data)
    assert len(data['result']['schedule_preview']) <= 5

def test_input_data_creation():
    """InputData створює правильну кількість об'єктів"""
    data = InputData(teachers_count=5, courses_count=10,
                     rooms_count=4, groups_count=3)
    assert len(data.teachers) == 5
    assert len(data.courses) == 10
    assert len(data.rooms) == 4
    assert len(data.groups) == 3


def test_input_data_total_slots():
    """slots_total = days_count * pairs_per_day"""
    data = InputData()
    assert data.slots_total == data.days_count * data.pairs_per_day


# ── GeneticScheduler unit tests ──────────────────────────────
def test_scheduler_creates_schedule():
    """Планувальник повертає розклад правильного розміру"""
    data = InputData(teachers_count=3, courses_count=5,
                     rooms_count=3, groups_count=2)
    scheduler = GeneticScheduler(data, pop_size=5, max_generations=3)
    result = scheduler.run()
    assert len(result) == 5


def test_scheduler_conflicts_non_negative():
    """_count_conflicts повертає невід'ємне число"""
    data = InputData(teachers_count=3, courses_count=5,
                     rooms_count=3, groups_count=2)
    scheduler = GeneticScheduler(data, pop_size=5, max_generations=3)
    individual = scheduler._random_individual()
    assert scheduler._count_conflicts(individual) >= 0


def test_scheduler_fitness_non_negative():
    """_fitness повертає невід'ємне число"""
    data = InputData(teachers_count=3, courses_count=5,
                     rooms_count=3, groups_count=2)
    scheduler = GeneticScheduler(data, pop_size=5, max_generations=3)
    individual = scheduler._random_individual()
    assert scheduler._fitness(individual) >= 0
