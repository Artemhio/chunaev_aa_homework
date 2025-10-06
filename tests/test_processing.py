import pytest
from datetime import datetime

from chunaev_aa_homework.processing import filter_by_state, sort_by_date


# Фикстура с тестовыми данными
@pytest.fixture
def sample_operations():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-01T12:30:00"},
        {"id": 2, "state": "CANCELED", "date": "2023-09-15T08:45:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-10-05T16:20:00"},
        {"id": 4, "state": "PENDING", "date": "2023-09-20T14:10:00"},
        {"id": 5, "date": "2023-08-10T11:00:00"},  # Нет статуса!
    ]

# Тесты для filter_by_state
def test_filter_executed(sample_operations):
    result = filter_by_state(sample_operations)
    assert len(result) == 2
    assert {op["id"] for op in result} == {1, 3}

def test_filter_canceled(sample_operations):
    result = filter_by_state(sample_operations, "CANCELED")
    assert len(result) == 1
    assert result[0]["id"] == 2

def test_filter_missing_state(sample_operations):
    result = filter_by_state(sample_operations)
    # Проверяем, что операция без статуса (id=5) не попала в результат
    assert all("state" in op for op in result)

# Тесты для sort_by_date
def test_sort_descending(sample_operations):
    # Фильтруем чтобы убрать элемент без статуса
    filtered_ops = [op for op in sample_operations if "state" in op]
    sorted_ops = sort_by_date(filtered_ops)

    dates = [op["date"] for op in sorted_ops]
    assert dates == [
        "2023-10-05T16:20:00",
        "2023-10-01T12:30:00",
        "2023-09-20T14:10:00",
        "2023-09-15T08:45:00"
    ]

def test_sort_ascending(sample_operations):
    filtered_ops = [op for op in sample_operations if "state" in op]
    sorted_ops = sort_by_date(filtered_ops, reverse=False)

    dates = [op["date"] for op in sorted_ops]
    assert dates == [
        "2023-09-15T08:45:00",
        "2023-09-20T14:10:00",
        "2023-10-01T12:30:00",
        "2023-10-05T16:20:00"
    ]

# Тест на обработку ошибок
def test_missing_date_key():
    with pytest.raises(KeyError):
        sort_by_date([{"state": "EXECUTED"}])  # Нет ключа "date"!