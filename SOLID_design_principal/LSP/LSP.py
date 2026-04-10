from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class DepositOnlyAccount(ABC):
    @abstractmethod
    def deposit(self, amount: float) -> None:
        raise NotImplementedError


class WithdrawableAccount(DepositOnlyAccount, ABC):
    @abstractmethod
    def withdraw(self, amount: float) -> None:
        raise NotImplementedError


class SavingAccount(WithdrawableAccount):
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


class CurrentAccount(WithdrawableAccount):
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


class FixedTermAccount(DepositOnlyAccount):
    def __init__(self) -> None:
        self._balance = 0.0

    def deposit(self, amount: float) -> None:
        self._balance += amount
        print(f"Deposited: {amount} in Fixed Term Account. New Balance: {self._balance}")


class BankClient:
    def __init__(
        self,
        withdrawable_accounts: List[WithdrawableAccount],
        deposit_only_accounts: List[DepositOnlyAccount],
    ) -> None:
        self._withdrawable_accounts = withdrawable_accounts
        self._deposit_only_accounts = deposit_only_accounts

    def process_transactions(self) -> None:
        for acc in self._withdrawable_accounts:
            acc.deposit(1000)
            acc.withdraw(500)

        for acc in self._deposit_only_accounts:
            acc.deposit(5000)


def main() -> None:
    withdrawable_accounts: List[WithdrawableAccount] = [SavingAccount(), CurrentAccount()]
    deposit_only_accounts: List[DepositOnlyAccount] = [FixedTermAccount()]

    client = BankClient(withdrawable_accounts, deposit_only_accounts)
    client.process_transactions()


if __name__ == "__main__":
    main()

