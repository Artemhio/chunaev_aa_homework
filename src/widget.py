from datetime import datetime
from typing import Any, Union

import masks

def mask_account_card(mask_account: str) -> Union[str, None]:
    """Функция обработки счетов или карт"""
    if "счет" in mask_account.lower():
        digits = "".join(filter(str.isdigit, mask_account))[-20:]
        return masks.get_mask_account(digits)
    else:
        digits = "".join(filter(str.isdigit, mask_account))[-16:]
        return masks.get_mask_card_number(digits)


def get_data(date_str: str) -> str:
    """Функция преобразования даты"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_obj.strftime("%d.%m.%Y")