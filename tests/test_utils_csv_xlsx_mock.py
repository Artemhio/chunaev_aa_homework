from unittest.mock import mock_open, patch

import pandas as pd

from chunaev_aa_homework.utils_io import (
    read_csv_operations,
    read_json,
    read_xlsx_operations,
)


def test_read_json_returns_loaded_data() -> None:
    fake_data = {"key": "value"}

    opened = mock_open()
    with patch("builtins.open", opened), patch(
        "json.load",
        return_value=fake_data,
    ) as json_load:
        result = read_json("data.json")

    opened.assert_called_once_with("data.json", encoding="utf-8")
    json_load.assert_called_once()
    assert result == fake_data


def test_read_csv_operations_uses_pandas_and_returns_records() -> None:
    dataframe = pd.DataFrame(
        [
            {"name": "Alice", "amount": 100},
            {"name": "Bob", "amount": 200},
        ],
    )

    with patch(
        "chunaev_aa_homework.utils_io.pd.read_csv",
        return_value=dataframe,
    ) as read_csv:
        result = read_csv_operations("operations.csv")

    read_csv.assert_called_once_with(
        "operations.csv",
        encoding="utf-8",
        delimiter=",",
    )
    assert result == dataframe.to_dict(orient="records")


def test_read_xlsx_operations_uses_pandas_and_returns_records() -> None:
    dataframe = pd.DataFrame(
        [
            {"id": 1, "amount": 100},
            {"id": 2, "amount": 200},
        ],
    )

    with patch(
        "chunaev_aa_homework.utils_io.pd.read_excel",
        return_value=dataframe,
    ) as read_excel:
        result = read_xlsx_operations("operations.xlsx")

    read_excel.assert_called_once_with(
        "operations.xlsx",
        sheet_name=0,
    )
    assert result == dataframe.to_dict(orient="records")


def test_read_xlsx_operations_with_custom_sheet_name() -> None:
    dataframe = pd.DataFrame([{"id": 1}])

    with patch(
        "chunaev_aa_homework.utils_io.pd.read_excel",
        return_value=dataframe,
    ) as read_excel:
        result = read_xlsx_operations(
            "operations.xlsx",
            sheet_name="Операции",
        )

    read_excel.assert_called_once_with(
        "operations.xlsx",
        sheet_name="Операции",
    )
    assert result == dataframe.to_dict(orient="records")
