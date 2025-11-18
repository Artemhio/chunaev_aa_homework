from unittest.mock import patch, mock_open

import pandas as pd
import pytest

from chunaev_aa_homework.utils import read_json, read_csv, read_xlsx


def test_read_json_returns_loaded_data():
    fake_data = {"key": "value"}

    m_open = mock_open()
    with patch("builtins.open", m_open), patch("json.load", return_value=fake_data) as mock_json_load:
        result = read_json("data.json")

    m_open.assert_called_once_with("data.json", encoding="utf-8")
    mock_json_load.assert_called_once()
    assert result == fake_data


def test_read_csv_uses_pandas_and_returns_records():
    fake_df = pd.DataFrame(
        [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30},
        ]
    )

    with patch("chunaev_aa_homework.utils.pd.read_csv", return_value=fake_df) as mock_read_csv:
        result = read_csv("data.csv")

    mock_read_csv.assert_called_once_with("data.csv", encoding="utf-8", delimiter=",")
    assert result == fake_df.to_dict(orient="records")


def test_read_xlsx_uses_pandas_and_returns_records():
    fake_df = pd.DataFrame(
        [
            {"id": 1, "value": "foo"},
            {"id": 2, "value": "bar"},
        ]
    )

    with patch("chunaev_aa_homework.utils.pd.read_excel", return_value=fake_df) as mock_read_excel:
        result = read_xlsx("data.xlsx")

    mock_read_excel.assert_called_once_with("data.xlsx", sheet_name=0)
    assert result == fake_df.to_dict(orient="records")


def test_read_xlsx_with_custom_sheet_name():
    fake_df = pd.DataFrame([{"id": 1}])

    with patch("chunaev_aa_homework.utils.pd.read_excel", return_value=fake_df) as mock_read_excel:
        result = read_xlsx("data.xlsx", sheet_name="Лист1")

    mock_read_excel.assert_called_once_with("data.xlsx", sheet_name="Лист1")
    assert result == fake_df.to_dict(orient="records")
