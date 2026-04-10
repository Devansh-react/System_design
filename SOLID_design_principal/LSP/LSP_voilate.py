from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class Account(ABC):
    @abstractmethod
    def deposit(self, amount: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        raise NotImplementedError


class SavingAccount(Account):
    def __init__(self) -> None:
        self._balance = 0.0

    def deposit(self, amount: float) -> None:
        self._balance += amount
        print(f"Deposited: {amount} in Savings Account. New Balance: {self._balance}")

    def withdraw(self, amount: float) -> None:
        if self._balance >= amount:
            self._balance -= amount
            print(f"Withdrawn: {amount} from Savings Account. New Balance: {self._balance}")
        else:
            print("Insufficient funds in Savings Account!")


class CurrentAccount(Account):
    def __init__(self) -> None:
        self._balance = 0.0

    def deposit(self, amount: float) -> None:
        self._balance += amount
        print(f"Deposited: {amount} in Current Account. New Balance: {self._balance}")

    def withdraw(self, amount: float) -> None:
        if self._balance >= amount:
            self._balance -= amount
            print(f"Withdrawn: {amount} from Current Account. New Balance: {self._balance}")
        else:
            print("Insufficient funds in Current Account!")


class FixedTermAccount(Account):
    def __init__(self) -> None:
        self._balance = 0.0

    def deposit(self, amount: float) -> None:
        self._balance += amount
        print(f"Deposited: {amount} in Fixed Term Account. New Balance: {self._balance}")

    def withdraw(self, amount: float) -> None:
        raise ValueError("Withdrawal not allowed in Fixed Term Account!")


class BankClient:
    def __init__(self, accounts: List[Account]) -> None:
        self._accounts = accounts

    def process_transactions(self) -> None:
        for acc in self._accounts:
            acc.deposit(1000)
            try:
                acc.withdraw(500)
            except ValueError as e:
                print(f"Exception: {e}")


def main() -> None:
    accounts: List[Account] = [SavingAccount(), CurrentAccount(), FixedTermAccount()]
    client = BankClient(accounts)
    client.process_transactions()


if __name__ == "__main__":
    main()

