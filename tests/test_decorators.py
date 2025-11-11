import pytest
from chunaev_aa_homework import log


def test_log_console_success(capsys):
    @log()
    def add(a, b):
        return a + b

    result = add(2, 3)
    captured = capsys.readouterr().out

    assert result == 5
    assert "Function 'add' executed successfully" in captured
    assert "Result: 5" in captured


def test_log_console_error(capsys):
    @log()
    def div(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(1, 0)

    captured = capsys.readouterr().out
    assert "Function 'div' raised ZeroDivisionError" in captured
    assert "args=(1, 0)" in captured


def test_log_file_success(tmp_path):
    logfile = tmp_path / "app.log"

    @log(filename=str(logfile))
    def mul(a, b):
        return a * b

    res = mul(3, 4)
    text = logfile.read_text(encoding="utf-8")

    assert res == 12
    assert "Function 'mul' executed successfully" in text
    assert "Result: 12" in text


def test_log_file_error(tmp_path):
    logfile = tmp_path / "errors.log"

    @log(filename=str(logfile))
    def boom():
        raise ValueError("bad")

    with pytest.raises(ValueError):
        boom()

    text = logfile.read_text(encoding="utf-8")
    assert "Function 'boom' raised ValueError" in text
    assert "kwargs={}" in text
