from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MenuItem:
    item_id: str
    name: str
    price: float

    def with_price(self, price: float) -> "MenuItem":
        return MenuItem(item_id=self.item_id, name=self.name, price=price)

