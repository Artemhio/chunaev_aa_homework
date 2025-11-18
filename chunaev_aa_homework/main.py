from __future__ import annotations

from typing import Any, Dict, List

from chunaev_aa_homework.operations_processing import (
    process_bank_operations,
    process_bank_search,
)
from chunaev_aa_homework.utils_io import (
    read_json,
    read_csv_operations,
    read_xlsx_operations,
)


Transaction = Dict[str, Any]

ALLOWED_STATUSES = ["EXECUTED", "CANCELED", "PENDING"]


def _ask_menu_choice() -> str:
    print(
        "Привет! Добро пожаловать в программу работы "
        "с банковскими транзакциями."
    )
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию из JSON-файла")
    print("2. Получить информацию из CSV-файла")
    print("3. Получить информацию из XLSX-файла")

    while True:
        choice = input("Ваш выбор: ").strip()
        if choice in {"1", "2", "3"}:
            return choice
        print("Некорректный пункт меню. Попробуйте снова.")


def _load_transactions(choice: str) -> List[Transaction]:
    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        return read_json("data/operations.json")

    if choice == "2":
        print("Для обработки выбран CSV-файл.")
        return read_csv_operations("data/operations.csv")

    if choice == "3":
        print("Для обработки выбран XLSX-файл.")
        return read_xlsx_operations("data/operations.xlsx")

    return []


def _ask_status() -> str:
    statuses = ", ".join(ALLOWED_STATUSES)

    while True:
        print("Введите статус для фильтрации.")
        print(f"Доступные статусы: {statuses}")

        status = input("Статус: ").strip().upper()

        if status in ALLOWED_STATUSES:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status

        print(f'Статус "{status}" недоступен.\n')


def _filter_by_status(
    data: List[Transaction],
    status: str,
) -> List[Transaction]:
    return [
        tx for tx in data
        if tx.get("state", "").upper() == status
    ]


def _ask_yes_no(prompt: str) -> bool:
    answer = input(f"{prompt} Да/Нет: ").strip().lower()
    return answer in ("да", "yes", "y")


def _sort_by_date(
    data: List[Transaction],
    ascending: bool,
) -> List[Transaction]:
    return sorted(
        data,
        key=lambda tx: tx.get("date", ""),
        reverse=not ascending,
    )


def _filter_rub_only(
    data: List[Transaction],
) -> List[Transaction]:
    result: List[Transaction] = []

    for tx in data:
        currency = (
            tx.get("operationAmount", {})
            .get("currency", {})
            .get("code", "")
        )
        if str(currency).upper() == "RUB":
            result.append(tx)

    return result


def _print_transactions(data: List[Transaction]) -> None:
    if not data:
        print(
            "Не найдено ни одной транзакции, подходящей "
            "под ваши условия фильтрации."
        )
        return

    print(f"\nВсего банковских операций в выборке: {len(data)}\n")

    for tx in data:
        date = tx.get("date", "")
        description = tx.get("description", "")
        amount_info = tx.get("operationAmount", {})
        amount = amount_info.get("amount", "")
        currency = amount_info.get("currency", {}).get("name", "")

        print(f"{date} {description}")
        print(f"Сумма: {amount} {currency}\n")


def main() -> None:
    choice = _ask_menu_choice()
    transactions = _load_transactions(choice)

    status = _ask_status()
    filtered = _filter_by_status(transactions, status)

    if _ask_yes_no("Отсортировать операции по дате?"):
        asc = _ask_yes_no("По возрастанию?")
        filtered = _sort_by_date(filtered, asc)

    if _ask_yes_no("Выводить только рублевые транзакции?"):
        filtered = _filter_rub_only(filtered)

    if _ask_yes_no("Фильтровать по слову в описании?"):
        word = input("Введите слово для поиска: ").strip()
        filtered = process_bank_search(filtered, word)

    print("Распечатываю итоговый список транзакций...")
    _print_transactions(filtered)
