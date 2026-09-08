"""Unit tests for the shared validators (input() is monkeypatched)."""

from utils.validators import get_valid_int, get_valid_float, confirm


def test_get_valid_int(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "42")
    assert get_valid_int("Enter: ") == 42


def test_get_valid_int_enforces_min(monkeypatch, capsys):
    responses = iter(["-5", "10"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    assert get_valid_int("Enter: ", min_value=0) == 10


def test_get_valid_float(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "3.14")
    assert get_valid_float("Enter: ") == 3.14


def test_confirm_default_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert confirm("Continue?") is True


def test_confirm_explicit_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert confirm("Continue?") is False
