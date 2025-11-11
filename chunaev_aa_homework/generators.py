from typing import Any, Dict, Iterable, Iterator


def filter_by_currency(
    transactions: Iterable[Dict[str, Any]],
    currency_code: str = "USD",
) -> Iterator[Dict[str, Any]]:
    """
    Итератор по транзакциям с указанной валютой.
    Возвращает только те записи, где код валюты совпадает с currency_code.
    """
    for tx in transactions:
        try:
            code = tx.get("operationAmount", {}) \
                     .get("currency", {}) \
                     .get("code")
            if code == currency_code:
                yield tx
        except AttributeError:
            continue


def transaction_descriptions(transactions):
    """Генератор, который возвращает описания операций с валютой."""
    for tx in transactions:
        desc = tx.get("description", "").strip()
        currency = (
            tx.get("operationAmount", {})
              .get("currency", {})
              .get("code", "")
              .strip()
        )
        if desc and currency:
            yield desc


def _format_card_number(n: int) -> str:
    """
    Вспомогательная функция: форматирует число в вид 'XXXX XXXX XXXX XXXX'.
    """
    s = f"{n:016d}"
    return f"{s[:4]} {s[4:8]} {s[8:12]} {s[12:]}"


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров карт в формате 'XXXX XXXX XXXX XXXX'.
    Диапазон включительный.
    Ограничение: 1 <= номер <= 9999 9999 9999 9999.
    """
    min_n = 1
    max_n = 9_999_999_999_999_999

    # Приводим начало и конец в допустимый диапазон
    if start < min_n:
        start = min_n
    if end > max_n:
        end = max_n

    if start > end:
        raise ValueError("start must be <= end")

    for n in range(start, end + 1):
        yield _format_card_number(n)
