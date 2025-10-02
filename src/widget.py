from datetime import datetime
from typing import Any, Union

from . import masks

def mask_account_card(mask_account: str) -> Union[str, None]:
    """Функция обработки счетов или карт"""
    if "счет" in mask_account.lower():
        digits = "".join(filter(str.isdigit, mask_account))[-20:]
        masked = get_mask_account(digits)
        # сохранить префикс ("Счет", "сЧеТ", как в исходной строке)
        prefix = mask_account.split()[0]
        return f"{prefix} {masked}"
    else:
        digits = "".join(filter(str.isdigit, mask_account))[-16:]
        masked = get_mask_card_number(digits)
        # сохранить префикс (например "Visa Platinum")
        prefix = " ".join(mask_account.split()[:-1])
        return f"{prefix} {masked}"


def get_data(date_str: str) -> str:
    """Функция преобразования даты"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_obj.strftime("%d.%m.%Y")