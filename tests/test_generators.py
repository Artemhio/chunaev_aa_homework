import pytest
from chunaev_aa_homework import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)

# ---------- фикстура с данными ----------
@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "250.00",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Оплата услуг",
        },
        {
            "id": 3,
            "operationAmount": {
                "amount": "50.50",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Покупка в магазине",
        },
        {"id": 4, "description": "Нет валюты"},  # некорректная структура — пропускаем
        {
            "id": 5,
            "operationAmount": {
                "amount": "1.00",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "",
        },
    ]


# ---------- filter_by_currency ----------
@pytest.mark.parametrize(
    "code, expected_ids",
    [
        ("USD", [1, 3, 5]),
        ("RUB", [2]),
        ("EUR", []),
    ],
)
def test_filter_by_currency(code, expected_ids, sample_transactions):
    result = list(filter_by_currency(sample_transactions, code))
    assert [tx["id"] for tx in result] == expected_ids


# ---------- transaction_descriptions ----------
def test_transaction_descriptions(sample_transactions):
    descs = list(transaction_descriptions(sample_transactions))
    assert descs == [
        "Перевод организации",
        "Оплата услуг",
        "Покупка в магазине",
    ]


# ---------- card_number_generator ----------
def test_card_number_generator_small_range():
    nums = list(card_number_generator(1, 3))
    assert nums == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
    ]
    assert all(len(s) == 19 for s in nums)
    assert all(s[4] == s[9] == s[14] == " " for s in nums)


def test_card_number_generator_bounds():
    first = next(card_number_generator(0, 1))  # 0 нормализуется до 1
    assert first == "0000 0000 0000 0001"


def test_card_number_generator_invalid_range():
    with pytest.raises(ValueError):
        _ = list(card_number_generator(5, 4))


def test_card_number_generator_too_large_start():
    with pytest.raises(ValueError):
        _ = list(card_number_generator(10**16 + 1, 10**16 + 2))