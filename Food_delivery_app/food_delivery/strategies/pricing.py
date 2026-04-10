from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from food_delivery.models.menu_item import MenuItem


class PriceCalculator(ABC):
    @abstractmethod
    def calc_total(self, items: Iterable[MenuItem]) -> float: ...


@dataclass(frozen=True, slots=True)
class SimplePriceCalculator(PriceCalculator):
    delivery_fee: float = 0.0
    tax_rate: float = 0.0  # e.g. 0.05 for 5%

    def calc_total(self, items: Iterable[MenuItem]) -> float:
        subtotal = sum(i.price for i in items)
        tax = subtotal * self.tax_rate
        total = subtotal + tax + self.delivery_fee
        return round(total, 2)

