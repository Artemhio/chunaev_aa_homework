from chunaev_aa_homework.operations_processing import (
    process_bank_operations,
    process_bank_search,
)


def test_process_bank_search_case_insensitive() -> None:
    data = [
        {"id": 1, "description": "Оплата мобильной связи"},
        {"id": 2, "description": "Перевод на карту"},
        {"id": 3, "description": "Магазин продуктов"},
    ]

    result = process_bank_search(data, "карт")
    ids = [item["id"] for item in result]

    assert ids == [2]


def test_process_bank_search_empty_input() -> None:
    data = [{"id": 1, "description": "Оплата"}]

    result = process_bank_search(data, "")

    assert result == []


def test_process_bank_operations_counts_categories() -> None:
    data = [
        {"description": "Оплата мобильной связи МТС"},
        {"description": "Оплата интернета"},
        {"description": "Перевод другу"},
        {"description": "Перевод на карту и оплата связи"},
    ]

    categories = ["связь", "перевод", "магазин"]

    result = process_bank_operations(data, categories)

    assert result == {
        "связь": 2,
        "перевод": 2,
        "магазин": 0,
    }


def test_process_bank_operations_empty_categories() -> None:
    data = [{"description": "Оплата"}]

    result = process_bank_operations(data, [])

    assert result == {}
