from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Tuple

from food_delivery.models.menu_item import MenuItem


@dataclass(slots=True)
class Cart:
    _items: Dict[str, Tuple[MenuItem, int]] = field(default_factory=dict)

    def add_item(self, item: MenuItem, qty: int = 1) -> None:
        if qty <= 0:
            raise ValueError("qty must be > 0")
        if item.item_id in self._items:
            existing, existing_qty = self._items[item.item_id]
            self._items[item.item_id] = (existing, existing_qty + qty)
        else:
            self._items[item.item_id] = (item, qty)

    def set_qty(self, item_id: str, qty: int) -> None:
        if qty < 0:
            raise ValueError("qty must be >= 0")
        if item_id not in self._items:
            raise KeyError(f"item_id not in cart: {item_id}")
        item, _ = self._items[item_id]
        if qty == 0:
            del self._items[item_id]
        else:
            self._items[item_id] = (item, qty)

    def remove_item(self, item_id: str) -> None:
        self._items.pop(item_id, None)

    def clear(self) -> None:
        self._items.clear()

    def items(self) -> List[Tuple[MenuItem, int]]:
        return list(self._items.values())

    def as_menu_items_expanded(self) -> List[MenuItem]:
        expanded: List[MenuItem] = []
        for item, qty in self._items.values():
            expanded.extend([item] * qty)
        return expanded

    def merge(self, items: Iterable[Tuple[MenuItem, int]]) -> None:
        for item, qty in items:
            self.add_item(item, qty=qty)

