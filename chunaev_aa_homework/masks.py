import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(
        LOG_DIR / "masks.log",
        mode="w",
        encoding="utf-8",
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def get_mask_card_number(number_card: str) -> str | None:
    """Функция маскировки номера карты с проверкой типа."""
    logger.info("Вызов get_mask_card_number")
    if not isinstance(number_card, str):
        logger.warning("number_card не str: %r", number_card)
        return None
    if number_card.isdigit() and len(number_card) == 16:
        masked = (
            f"{number_card[:4]} {number_card[4:6]}** **** {number_card[12:]}"
        )
        logger.info("Успешная маскировка номера карты")
        return masked
    logger.warning("Неверный формат номера карты: %r", number_card)
    return None


def get_mask_account(number_score: str) -> str | None:
    """Функция маскировки номера счета с проверкой типа."""
    logger.info("Вызов get_mask_account")
    if not isinstance(number_score, str):
        logger.warning("number_score не str: %r", number_score)
        return None
    if number_score.isdigit() and len(number_score) == 20:
        masked = f"**{number_score[-4:]}"
        logger.info("Успешная маскировка счета")
        return masked
    logger.warning("Неверный формат счета: %r", number_score)
    return None
