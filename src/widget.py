from datetime import datetime
from typing import Any

import masks


def mask_account_card(mask_account: str) -> Any:
    """Функция обработки счетов или карт"""
    bank_account = "Счет"
    bank_account_lower = bank_account.lower()
    if bank_account_lower in mask_account:
        account = mask_account[-20:]
        return mask_account[:-20] + masks.get_mask_account(account)
    else:
        card_number = "".join(mask_account[-16:].split())
        return mask_account[:-16] + masks.get_mask_card_number(card_number)


def get_data(user_data: str) -> str:
    """Функция преобразования даты"""
    date_it = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    formated_date = date_it.strptime("%d.%m.%Y")
    return formated_date
