from __future__ import annotations


class BankAccount:
    # Invariant: balance cannot be negative
    def __init__(self, balance: float) -> None:
        if balance < 0:
            raise ValueError("Balance can't be negative")
        self.balance = balance

    def withdraw(self, amount: float) -> None:
        if self.balance - amount < 0:
            raise RuntimeError("Insufficient funds")
        self.balance -= amount
        print(f"Amount withdrawn. Remaining balance is {self.balance}")


class CheatAccount(BankAccount):
    # Breaks invariant: allows negative balance (LSP violation)
    def withdraw(self, amount: float) -> None:
        self.balance -= amount
        print(f"Amount withdrawn. Remaining balance is {self.balance}")


def main() -> None:
    bank_account = BankAccount(100)
    bank_account.withdraw(100)


if __name__ == "__main__":
    main()

