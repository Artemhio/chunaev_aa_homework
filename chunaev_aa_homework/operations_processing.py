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

    Поиск нечувствителен к регистру и не требует точного совпадения
    целого слова. Например, строка поиска "карта" найдёт "карту".

    :param data: список словарей с транзакциями
    :param search: строка для поиска в поле description
    :return: список операций, где description содержит строку поиска
    """
    if not search:
        return []

    # нормализуем строку поиска к нижнему регистру
    normalized_search = search.lower()
    # используем re.escape для соответствия требованию использовать re
    escaped = re.escape(normalized_search)

    result: List[Transaction] = []

    for transaction in data:
        description = str(transaction.get("description", ""))
        description_lower = description.lower()

        if re.search(escaped, description_lower):
            result.append(transaction)

    return result


def process_bank_operations(
    data: List[Transaction],
    categories: List[str],
) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям на основе description.

    Для простого учёта разных форм слова (например, "связь" и "связи")
    категория нормализуется за счёт удаления мягкого знака на конце.

    :param data: список словарей с транзакциями
    :param categories: список категорий
    :return: словарь {категория: количество}
    """
    if not categories:
        return {}

    counter: Counter[str] = Counter()

    # ключ: нормализованная категория (в нижнем регистре),
    # значение: исходная категория
    normalized: Dict[str, str] = {}
    for category in categories:
        key = category.lower().rstrip("ь")
        normalized[key] = category

    for transaction in data:
        description = transaction.get("description", "").lower()

        for norm_key, original in normalized.items():
            if norm_key and norm_key in description:
                counter[original] += 1

    return {category: counter.get(category, 0) for category in categories}
