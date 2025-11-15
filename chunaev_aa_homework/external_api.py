import os
import requests
from dotenv import load_dotenv

load_dotenv()


def amount_in_rub(transaction: dict) -> float:
    """
    Возвращает сумму транзакции в рублях (float).

    Если валюта RUB — возвращает сумму как есть.
    Для USD и EUR делает запрос к API конвертации
    и использует поле "result" из ответа.
    """
    try:
        amount = float(transaction["operationAmount"]["amount"])
        code = transaction["operationAmount"]["currency"]["code"].upper()

        # если уже рубли — ничего не конвертируем
        if code == "RUB":
            return amount

        if code not in ("USD", "EUR"):
            # по заданию работаем только с USD/EUR
            raise ValueError(f"Unsupported currency: {code}")

        api_key = os.getenv("EXCHANGE_RATES_API_KEY")
        url = os.getenv(
            "EXCHANGE_RATES_API_URL",
            "https://api.apilayer.com/exchangerates_data/convert",
        )

        if not api_key or not url:
            print("Не найден API ключ или URL в .env")
            return 0.0

        headers = {"apikey": api_key}
        params = {"from": code, "to": "RUB", "amount": amount}

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        result = data.get("result")

        if result is None:
            print("В ответе API нет поля 'result'")
            return 0.0

        return float(result)

    except Exception as e:
        print(f"Ошибка при конвертации валюты: {e}")
        return 0.0
