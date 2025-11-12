import os
import requests
from dotenv import load_dotenv

load_dotenv()


def amount_in_rub(transaction: dict) -> float:
    """Возвращает сумму транзакции в рублях (float)."""
    amount = float(transaction["operationAmount"]["amount"])
    code = transaction["operationAmount"]["currency"]["code"].upper()

    if code == "RUB":
        return amount

    if code in ("USD", "EUR"):
        api_key = os.getenv("EXCHANGE_RATES_API_KEY")
        url = os.getenv("EXCHANGE_RATES_API_URL")
        headers = {"apikey": api_key}
        params = {"base": code, "symbols": "RUB"}

        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        rate = data["rates"]["RUB"]
        return amount * rate

    raise ValueError("Unsupported currency")
