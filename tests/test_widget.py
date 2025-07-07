import pytest

import sys

import os

from src.widget import mask_account_card, get_data

# Тестовые данные
SAMPLE_CARD = "Visa Platinum 1234567890123456"
SAMPLE_ACCOUNT = "Счет 12345678901234567890"
SHORT_ACCOUNT = "Счет 123"

# Тесты для mask_account_card
def test_mask_card():
    assert mask_account_card(SAMPLE_CARD) == "Visa Platinum 1234 56** **** 3456"

def test_mask_account():
    assert mask_account_card(SAMPLE_ACCOUNT) == "Счет **7890"

def test_mask_invalid_account():
    assert mask_account_card(SHORT_ACCOUNT) is None

def test_mask_case_insensitive():
    assert mask_account_card("сЧеТ 12345678901234567890") == "сЧеТ **7890"

# Тесты для get_data
def test_date_conversion():
    assert get_data("2023-10-05T16:20:00.000000Z") == "05.10.2023"

def test_date_with_microseconds():
    assert get_data("2022-12-31T23:59:59.999999Z") == "31.12.2022"

def test_invalid_date_format():
    with pytest.raises(ValueError):
        get_data("2023/10/05 16:20:00")