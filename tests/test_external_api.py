import pytest
from chunaev_aa_homework.external_api import amount_in_rub


def test_rub_transaction():
    tx = {"operationAmount": {"amount": "100.0", "currency": {"code": "RUB"}}}
    assert amount_in_rub(tx) == 100.0


def test_usd_conversion(monkeypatch):
    import chunaev_aa_homework.external_api as api

    def fake_get(url, headers, params, timeout):
        class Resp:
            def json(self):
                return {"rates": {"RUB": 90.0}}
        return Resp()

    monkeypatch.setattr(api.requests, "get", fake_get)
    monkeypatch.setenv("EXCHANGE_RATES_API_KEY", "fake")
    monkeypatch.setenv("EXCHANGE_RATES_API_URL", "fake_url")

    tx = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}
    assert amount_in_rub(tx) == 900.0


def test_unsupported_currency():
    tx = {"operationAmount": {"amount": "10", "currency": {"code": "KZT"}}}
    with pytest.raises(ValueError):
        amount_in_rub(tx)
