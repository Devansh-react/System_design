from __future__ import annotations


class BankAccount:
    def __init__(self, balance: float) -> None:
        if balance < 0:
            raise ValueError("Balance can't be negative")
        self.balance = balance

    # History constraint: withdraw is allowed
    def withdraw(self, amount: float) -> None:
        if self.balance - amount < 0:
            raise RuntimeError("Insufficient funds")
        self.balance -= amount
        print(f"Amount withdrawn. Remaining balance is {self.balance}")


class FixedDepositAccount(BankAccount):
    # Breaks history constraint: now withdraw is not allowed (LSP violation)
    def withdraw(self, amount: float) -> None:
        raise RuntimeError("Withdraw not allowed in Fixed Deposit")


def main() -> None:
    bank_account = BankAccount(100)
    bank_account.withdraw(100)


if __name__ == "__main__":
    main()

