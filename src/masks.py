def get_mask_card_number(number_card: str) -> str | None:
    """Функция маскировки номера карты"""
    if number_card.isdigit() and len(number_card) == 16:
        return f"{number_card[:4]} {number_card[5:7]}** **** {number_card[12:]}"
    else:
        return None


def get_mask_account(number_score: str) -> str | None:
    """Функция маскировки номера счета"""
    if number_score.isdigit() and len(number_score) == 20:
        return f"**{number_score[-4::]}"
    else:
        return None
