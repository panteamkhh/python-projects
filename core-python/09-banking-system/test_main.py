"""Unit tests for Account and Bank."""

import pytest
from main import Account, Bank, InsufficientFundsError


def test_deposit_increases_balance():
    account = Account("A1", "Ali", balance=100)
    account.deposit(50)
    assert account.balance == 150


def test_withdraw_decreases_balance():
    account = Account("A1", "Ali", balance=100)
    account.withdraw(40)
    assert account.balance == 60


def test_withdraw_raises_when_insufficient_funds():
    account = Account("A1", "Ali", balance=10)
    with pytest.raises(InsufficientFundsError):
        account.withdraw(50)


def test_bank_create_account_and_duplicate(tmp_path):
    bank = Bank(file_name=str(tmp_path / "accounts.json"))
    bank.create_account("A1", "Ali")
    with pytest.raises(ValueError):
        bank.create_account("A1", "Reza")


def test_bank_transfer(tmp_path):
    bank = Bank(file_name=str(tmp_path / "accounts.json"))
    bank.create_account("A1", "Ali")
    bank.create_account("A2", "Sara")
    bank.get_account("A1").deposit(100)

    bank.transfer("A1", "A2", 30)

    assert bank.get_account("A1").balance == 70
    assert bank.get_account("A2").balance == 30
