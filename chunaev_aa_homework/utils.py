import json
from pathlib import Path


def load_transactions(path: str) -> list[dict]:
    """Читает JSON-файл и возвращает список транзакций."""
    file = Path(path)

    if not file.exists() or file.is_dir():
        return []

    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []
