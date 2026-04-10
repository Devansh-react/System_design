from __future__ import annotations

from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str: ...


class UpiPayment(PaymentStrategy):
    def __init__(self, upi_id: str) -> None:
        self.upi_id = upi_id

    def pay(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("amount must be > 0")
        return f"PAID {amount:.2f} via UPI({self.upi_id})"


class CardPayment(PaymentStrategy):
    def __init__(self, last4: str) -> None:
        if len(last4) != 4 or not last4.isdigit():
            raise ValueError("last4 must be 4 digits")
        self.last4 = last4

    def pay(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("amount must be > 0")
        return f"PAID {amount:.2f} via CARD(****{self.last4})"


class NetBankingPayment(PaymentStrategy):
    def __init__(self, bank_name: str) -> None:
        self.bank_name = bank_name

    def pay(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("amount must be > 0")
        return f"PAID {amount:.2f} via NET_BANKING({self.bank_name})"

