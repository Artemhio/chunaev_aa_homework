import requests

import chunaev_aa_homework.external_api as api


def test_amount_in_rub_passthrough_rub():
    tx = {"operationAmount": {"amount": "123.45", "currency": {"code": "RUB"}}}
    assert api.amount_in_rub(tx) == 123.45


def test_amount_in_rub_usd(monkeypatch):
    def fake_get(url, headers, params, timeout):
        # Проверим, что мы действительно передаём base и symbols
        assert params["base"] == "USD"
        assert params["symbols"] == "RUB"

        class Resp:
            def raise_for_status(self):  # имитируем 200 OK
                pass

            def json(self):
                return {"rates": {"RUB": 90.0}}

        return Resp()

    monkeypatch.setenv("EXCHANGE_RATES_API_KEY", "fake")
    monkeypatch.setenv("EXCHANGE_RATES_API_URL", "https://api.example/latest")
    monkeypatch.setattr(api.requests, "get", fake_get)

    tx = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}
    assert api.amount_in_rub(tx) == 900.00  # round(..., 2) в функции


def test_amount_in_rub_eur(monkeypatch):
    def fake_get(url, headers, params, timeout):
        assert params["base"] == "EUR"
        assert params["symbols"] == "RUB"

        class Resp:
            def raise_for_status(self):
                pass

            def json(self):
                return {"rates": {"RUB": 98.5}}

        return Resp()

    monkeypatch.setenv("EXCHANGE_RATES_API_KEY", "fake")
    monkeypatch.setenv("EXCHANGE_RATES_API_URL", "https://api.example/latest")
    monkeypatch.setattr(api.requests, "get", fake_get)

    tx = {"operationAmount": {"amount": "2", "currency": {"code": "EUR"}}}
    assert api.amount_in_rub(tx) == 197.0


def test_amount_in_rub_missing_env(monkeypatch):
    # Нет ключа/URL → функция вернёт 0.0
    monkeypatch.delenv("EXCHANGE_RATES_API_KEY", raising=False)
    monkeypatch.delenv("EXCHANGE_RATES_API_URL", raising=False)

    tx = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}
    assert api.amount_in_rub(tx) == 0.0


def test_amount_in_rub_http_error(monkeypatch):
    def fake_get(url, headers, params, timeout):
        class Resp:
            def raise_for_status(self):
                raise requests.HTTPError("Boom")

            def json(self):
                return {}

        return Resp()

    monkeypatch.setenv("EXCHANGE_RATES_API_KEY", "fake")
    monkeypatch.setenv("EXCHANGE_RATES_API_URL", "https://api.example/latest")
    monkeypatch.setattr(api.requests, "get", fake_get)

    tx = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}
    assert api.amount_in_rub(tx) == 0.0


def test_amount_in_rub_unsupported_currency(monkeypatch):
    # В функции сейчас: при не USD/EUR → ValueError внутри try → возврат 0.0
    tx = {"operationAmount": {"amount": "10", "currency": {"code": "KZT"}}}
    assert api.amount_in_rub(tx) == 0.0
