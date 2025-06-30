import pytest

from src.masks import get_mask_card_number, get_mask_account


# Тесты для маскировки карт
def test_get_mask_card_number_valid():
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"

def test_get_mask_card_number_invalid_length():
    assert get_mask_card_number("12345") is None  # Слишком короткий
    assert get_mask_card_number("12345678901234567890") is None  # Слишком длинный

def test_get_mask_card_number_non_digit():
    assert get_mask_card_number("1234abcd56789012") is None  # Содержит буквы
    assert get_mask_card_number("1234 5678 9012 3456") is None  # Содержит пробелы

# Тесты для маскировки счетов
def test_get_mask_account_valid():
    assert get_mask_account("12345678901234567890") == "**7890"

def test_get_mask_account_invalid_length():
    assert get_mask_account("12345") is None  # Слишком короткий
    assert get_mask_account("123456789012345678901234") is None  # Слишком длинный

def test_get_mask_account_non_digit():
    assert get_mask_account("1234567890abcdefghij") is None  # Содержит буквы
    assert get_mask_account("12345 67890 12345 67890") is None  # Содержит пробелы

# Тест на граничное условие для карт
def test_card_edge_cases():
    assert get_mask_card_number("") is None  # Пустая строка
    assert get_mask_card_number(None) is None  # None (опционально)

# Тест на граничное условие для счетов
def test_account_edge_cases():
    assert get_mask_account("") is None  # Пустая строка
    assert get_mask_account(None) is None  # None (опционально)