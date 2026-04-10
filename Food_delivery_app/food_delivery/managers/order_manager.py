from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from food_delivery.models.order import Order
from food_delivery.utils.singleton import SingletonMeta


@dataclass
class OrderManager(metaclass=SingletonMeta):
    _orders: Dict[str, Order] = field(default_factory=dict)

    def add_order(self, order: Order) -> None:
        if order.order_id in self._orders:
            raise ValueError(f"Order already exists: {order.order_id}")
        self._orders[order.order_id] = order

    def get_order(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)

    def list_orders(self) -> List[Order]:
        return list(self._orders.values())

    def save_to_db(self) -> None:
        # Placeholder for persistence.
        return None

