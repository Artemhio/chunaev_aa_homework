from __future__ import annotations

import re
from collections import Counter
from typing import Any, Dict, List

Transaction = Dict[str, Any]


def process_bank_search(
    data: List[Transaction],
    search: str,
) -> List[Transaction]:
    """
    Ищет операции по подстроке в описании с использованием re.

    :param data: список словарей с транзакциями
    :param search: строка для поиска в поле description
    :return: список операций, где description содержит строку поиска
    """
    if not search:
        return []

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result: List[Transaction] = []

    for transaction in data:
        description = transaction.get("description", "")
        if pattern.search(description):
            result.append(transaction)

    return result


def process_bank_operations(
    data: List[Transaction],
    categories: List[str],
) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям на основе description.

    :param data: список словарей с транзакциями
    :param categories: список категорий
    :return: словарь {категория: количество}
    """
    if not categories:
        return {}

    counter: Counter[str] = Counter()
    lowered = {cat.lower(): cat for cat in categories}

    for transaction in data:
        description = transaction.get("description", "").lower()

        for lower_cat, original in lowered.items():
            if lower_cat in description:
                counter[original] += 1

    return {category: counter.get(category, 0) for category in categories}
