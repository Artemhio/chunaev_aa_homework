import pytest
from src.widget import mask_account_card, get_data

# ================================
# Фикстура для повторяющихся данных
# ================================
@pytest.fixture
def sample_data():
    return {
        "card": "Visa Platinum 1234567890123456",
        "account": "Счет 12345678901234567890",
        "short_account": "123",
        "case_insensitive_account": "сЧеТ 12345678901234567890"
    }


# ================================
# Тест маскировки карт с параметризацией
# ================================
@pytest.mark.parametrize(
    "input_card, expected_masked",
    [
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("MasterCard 9876543210987654", "MasterCard 9876 54** **** 7654"),
    ]
)
def test_mask_card_param(input_card, expected_masked):
    assert mask_account_card(input_card) == expected_masked


# ================================
# Тест маскировки счетов с параметризацией
# ================================
@pytest.mark.parametrize(
    "input_account, expected_masked",
    [
        ("Счет 12345678901234567890", "Счет **7890"),
        ("СЧЕТ 09876543210987654321", "СЧЕТ **4321"),
    ]
)
def test_mask_account_param(input_account, expected_masked):
    assert mask_account_card(input_account) == expected_masked


# ================================
# Тесты с фикстурой (твой старый стиль)
# ================================
def test_mask_account_fixture(sample_data):
    assert mask_account_card(sample_data["account"]) == "Счет **7890"
    assert mask_account_card(sample_data["short_account"]) is None
    assert mask_account_card(sample_data["case_insensitive_account"]) == "сЧеТ **7890"


# ================================
# Тесты даты с параметризацией
# ================================
@pytest.mark.parametrize(
    "input_date, expected_output",
    [
        ("2023-03-22T10:45:12.123456Z", "22.03.2023"),
        ("2022-12-01T00:00:00.000000Z", "01.12.2022"),
    ]
)
def test_date_conversion_param(input_date, expected_output):
    assert get_data(input_date) == expected_output


def test_invalid_date_format():
    with pytest.raises(ValueError):
        get_data("01.01.2023")
