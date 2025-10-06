def get_mask_card_number(number_card: str) -> str | None:
    """Функция маскировки номера карты с проверкой типа"""
    if not isinstance(number_card, str):
        return None
    if number_card.isdigit() and len(number_card) == 16:
        return (
            f"{number_card[:4]} {number_card[4:6]}** **** "
            f"{number_card[12:]}"
        )
    return None


def get_mask_account(number_score: str) -> str | None:
    """Функция маскировки номера счета с проверкой типа"""
    if not isinstance(number_score, str):
        return None
    if number_score.isdigit() and len(number_score) == 20:
        return f"**{number_score[-4:]}"
    return None
