import requests
import chunaev_aa_homework.external_api as api


def test_amount_in_rub_passthrough_rub():
    tx = {"operationAmount": {"amount": "123.45", "currency": {"code": "RUB"}}}
    assert api.amount_in_rub(tx) == 123.45


def test_amount_in_rub_usd(monkeypatch):
    def fake_get(url, headers, params, timeout):
        assert params["from"] == "USD"
        assert params["to"] == "RUB"
        assert params["amount"] == 10.0

        class Resp:
            def raise_for_status(self):
                pass

            def json(self):
                # имитируем ответ API /convert
                return {"result": 950.5}

        return Resp()

    monkeypatch.setenv("EXCHANGE_RATES_API_KEY", "fake")
    monkeypatch.setenv("EXCHANGE_RATES_API_URL", "https://api.example/convert")
    monkeypatch.setattr(api.requests, "get", fake_get)

    tx = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}
    assert api.amount_in_rub(tx) == 950.5


def test_amount_in_rub_eur(monkeypatch):
    def fake_get(url, headers, params, timeout):
        assert params["from"] == "EUR"
        assert params["to"] == "RUB"
        assert params["amount"] == 2.0

        class Resp:
            def raise_for_status(self):
                pass

            def json(self):
                return {"result": 197.0}

        return Resp()

    monkeypatch.setenv("EXCHANGE_RATES_API_KEY", "fake")
    monkeypatch.setenv("EXCHANGE_RATES_API_URL", "https://api.example/convert")
    monkeypatch.setattr(api.requests, "get", fake_get)

    tx = {"operationAmount": {"amount": "2", "currency": {"code": "EUR"}}}
    assert api.amount_in_rub(tx) == 197.0


def test_amount_in_rub_missing_env(monkeypatch):
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
    monkeypatch.setenv("EXCHANGE_RATES_API_URL", "https://api.example/convert")
    monkeypatch.setattr(api.requests, "get", fake_get)

    tx = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}
    assert api.amount_in_rub(tx) == 0.0


def test_amount_in_rub_unsupported_currency():
    tx = {"operationAmount": {"amount": "10", "currency": {"code": "KZT"}}}
    # внутри будет ValueError, который поймается в except → вернется 0.0
    assert api.amount_in_rub(tx) == 0.0
