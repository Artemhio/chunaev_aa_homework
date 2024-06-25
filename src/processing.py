from typing import Any


def filter_by_state(states_in: list[dict[str, Any]], state_id: str = "EXECUTED") -> list[dict[str, Any]]:
    """Функция фильтрации операций по ключу state"""
    list_state = []
    for key in states_in:
        if key.get("state") == state_id:
            list_state.append(key)
    return list_state


def sort_by_date(states_in: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Функция сортировки операций по дате"""
    sorted_inform_state = sorted(states_in, key=lambda states_in: states_in["date"], reverse=reverse)
    return sorted_inform_state
