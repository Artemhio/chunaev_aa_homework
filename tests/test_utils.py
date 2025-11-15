import json

from chunaev_aa_homework.utils import load_transactions


def test_load_transactions_ok(tmp_path):
    data = [{"id": 1}, {"id": 2}]
    f = tmp_path / "data.json"
    f.write_text(json.dumps(data), encoding="utf-8")
    assert load_transactions(f) == data


def test_load_transactions_empty(tmp_path):
    f = tmp_path / "empty.json"
    f.write_text("", encoding="utf-8")
    assert load_transactions(f) == []


def test_load_transactions_not_list(tmp_path):
    f = tmp_path / "data.json"
    f.write_text(json.dumps({"a": 1}), encoding="utf-8")
    assert load_transactions(f) == []
