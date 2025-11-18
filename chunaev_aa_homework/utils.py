import json
import logging
from pathlib import Path
from typing import Any, Dict, List
import pandas as pd


LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(
        LOG_DIR / "utils.log",
        mode="w",
        encoding="utf-8",
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def load_transactions(path: str) -> list[dict]:
    """Читает JSON-файл и возвращает список транзакций.

    Если файл не найден, это директория, JSON пустой/битый
    или в корне не список — возвращает пустой список.
    """
    file = Path(path)
    logger.info("Чтение JSON-файла: %s", file)

    if not file.exists() or file.is_dir():
        logger.error("Файл не найден или это директория: %s", file)
        return []

    try:
        with file.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        logger.error("Ошибка разбора JSON в файле: %s", file)
        return []
    except OSError as exc:
        logger.error("Ошибка при чтении файла %s: %s", file, exc)
        return []

    if not isinstance(data, list):
        logger.warning(
            "Ожидался список транзакций, но получен тип: %s",
            type(data),
        )
        return []

    logger.info("Успешно прочитан файл. Количество транзакций: %d", len(data))
    return data


def read_json(path: str | Path) -> Any:
    """
    Простой читатель JSON-файла.
    Возвращает то, что вернул json.load (словарь, список и т.п.).
    """
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def read_csv(
    path: str | Path,
    *,
    encoding: str = "utf-8",
    delimiter: str = ",",
) -> List[Dict[str, Any]]:
    """
    Читает CSV-файл через pandas и возвращает список словарей (records).
    """
    df = pd.read_csv(path, encoding=encoding, delimiter=delimiter)
    return df.to_dict(orient="records")


def read_xlsx(
    path: str | Path,
    *,
    sheet_name: int | str | None = 0,
) -> List[Dict[str, Any]]:
    """
    Читает XLSX-файл через pandas и возвращает список словарей (records).
    """
    df = pd.read_excel(path, sheet_name=sheet_name)
    return df.to_dict(orient="records")
