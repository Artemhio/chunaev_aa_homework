import pytest
from datetime import datetime
from src.widget import mask_account_card, get_data

# Тестовые данные
VALID_CARD = "Visa Platinum 1234567890123456"
VALID_ACCOUNT = "Счет 12345678901234567890"
MIXED_CASE_ACCOUNT = "сЧеТ 12345678901234567890"
CARD_WITH_SPACES = "MasterCard 1234 5678 9012 3456"
SHORT_ACCOUNT = "Счет 123"
INVALID_ACCOUNT = "Счет невалидный"
NO_DIGITS = "Только текст"
EMPTY_STRING = ""

# Тесты для mask_account_card()
def test_mask_valid_card():
    """Тест маскировки валидной карты"""
    assert mask_account_card(VALID_CARD) == "Visa Platinum 1234 56** **** 3456"

def test_mask_valid_account():
    """Тест маскировки валидного счета"""
    assert mask_account_card(VALID_ACCOUNT) == "Счет **7890"

def test_mask_account_case_insensitive():
    """Тест нечувствительности к регистру"""
    assert mask_account_card(MIXED_CASE_ACCOUNT) == "сЧеТ **7890"

def test_mask_card_with_spaces():
    """Тест обработки карты с пробелами"""
    assert mask_account_card(CARD_WITH_SPACES) == "MasterCard 1234 56** **** 3456"

def test_mask_short_account():
    """Тест слишком короткого счета"""
    assert mask_account_card(SHORT_ACCOUNT) is None

def test_mask_account_without_digits():
    """Тест счета без цифр"""
    assert mask_account_card(INVALID_ACCOUNT) is None

def test_mask_no_digits_string():
    """Тест строки без цифр"""
    assert mask_account_card(NO_DIGITS) is None

def test_mask_empty_string():
    """Тест пустой строки"""
    assert mask_account_card(EMPTY_STRING) is None

# Тесты для get_data()
def test_date_conversion():
    """Тест преобразования валидной даты"""
    assert get_data("2023-10-05T16:20:00.000000Z") == "05.10.2023"

def test_date_with_microseconds():
    """Тест даты с микросекундами"""
    assert get_data("2022-12-31T23:59:59.999999Z") == "31.12.2022"

def test_date_different_format():
    """Тест даты в неожиданном формате"""
    with pytest.raises(ValueError):
        get_data("2023/10/05 16:20:00")

def test_date_invalid_string():
    """Тест невалидной строки даты"""
    with pytest.raises(ValueError):
        get_data("не дата")

def test_date_empty_string():
    """Тест пустой строки"""
    with pytest.raises(ValueError):
        get_data("")

# Параметризованные тесты для обработки граничных случаев
@pytest.mark.parametrize("input_str, expected", [
    ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
    ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
    ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
    ("Счет 00000000000000000001", "Счет **0001"),
    ("Карта 1234 5678 9012 3456", "Карта 1234 56** **** 3456"),
])
def test_various_card_formats(input_str, expected):
    assert mask_account_card(input_str) == expected

# Тест обработки None
def test_mask_none_input():
    """Тест обработки None вместо строки"""
    assert mask_account_card(None) is None