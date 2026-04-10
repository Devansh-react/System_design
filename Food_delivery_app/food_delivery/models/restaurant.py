from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional

from food_delivery.models.menu_item import MenuItem


@dataclass(slots=True)
class Restaurant:
    restaurant_id: str
    name: str
    address: str
    location: str
    menu_items: List[MenuItem] = field(default_factory=list)

    def add_menu_item(self, item: MenuItem) -> None:
        self.menu_items.append(item)

    def remove_menu_item(self, item_id: str) -> bool:
        before = len(self.menu_items)
        self.menu_items = [i for i in self.menu_items if i.item_id != item_id]
        return len(self.menu_items) != before

    def get_menu_item(self, item_id: str) -> Optional[MenuItem]:
        for item in self.menu_items:
            if item.item_id == item_id:
                return item
        return None

    def set_menu_items(self, items: Iterable[MenuItem]) -> None:
        self.menu_items = list(items)

