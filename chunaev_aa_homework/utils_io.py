from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import json
import pandas as pd


JsonDict = Dict[str, Any]
JsonList = List[JsonDict]


def read_json(path: str | Path) -> Any:
    """
    Читает JSON-файл и возвращает результат json.load.

    :param path: путь к JSON-файлу
    :return: данные из файла (словарь, список и т.п.)
    """
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def read_csv_operations(
    path: str | Path,
    *,
    encoding: str = "utf-8",
    delimiter: str = ",",
) -> JsonList:
    """
    Читает CSV-файл с финансовыми операциями.

    :param path: путь к CSV-файлу
    :param encoding: кодировка файла
    :param delimiter: разделитель колонок
    :return: список словарей с транзакциями
    """
    dataframe = pd.read_csv(
        path,
        encoding=encoding,
        delimiter=delimiter,
    )
    return dataframe.to_dict(orient="records")


def read_xlsx_operations(
    path: str | Path,
    *,
    sheet_name: int | str | None = 0,
) -> JsonList:
    """
    Читает Excel-файл с финансовыми операциями.

    :param path: путь к Excel-файлу
    :param sheet_name: имя или номер страницы
    :return: список словарей с транзакциями
    """
    dataframe = pd.read_excel(
        path,
        sheet_name=sheet_name,
    )
    return dataframe.to_dict(orient="records")
