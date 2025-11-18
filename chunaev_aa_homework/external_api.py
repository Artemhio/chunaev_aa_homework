import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_API_URL = "https://api.apilayer.com/exchangerates_data/convert"


def amount_in_rub(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях (float).

    Если валюта RUB — возвращает сумму как есть.
    Для USD и EUR делает запрос к API конвертации
    и использует поле "result" из ответа.

    В случае ошибки возвращает 0.0.
    """
    try:
        amount = float(transaction["operationAmount"]["amount"])
        code = transaction["operationAmount"]["currency"]["code"].upper()

        if code == "RUB":
            return amount

        if code not in ("USD", "EUR"):
            raise ValueError(f"Unsupported currency: {code}")

        api_key = os.getenv("EXCHANGE_RATES_API_KEY")

        if not api_key:
            print("Не найден API-ключ EXCHANGE_RATES_API_KEY в .env")
            return 0.0

        headers = {"apikey": api_key}
        params = {"from": code, "to": "RUB", "amount": amount}

        response = requests.get(
            EXCHANGE_API_URL,
            headers=headers,
            params=params,
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()
        result = data.get("result")

        if result is None:
            print("В ответе API нет поля 'result'")
            return 0.0

        return float(result)

    except requests.HTTPError as error:
        print(f"Ошибка HTTP при конвертации валюты: {error}")
        return 0.0
    except Exception as error:
        print(f"Ошибка при конвертации валюты: {error}")
        return 0.0
