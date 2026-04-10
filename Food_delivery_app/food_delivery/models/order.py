from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import List, Optional, Sequence

from food_delivery.models.menu_item import MenuItem
from food_delivery.models.restaurant import Restaurant
from food_delivery.models.user import User
from food_delivery.strategies.delivery import DeliveryMethod
from food_delivery.strategies.payment import PaymentStrategy
from food_delivery.strategies.pricing import PriceCalculator


@dataclass(slots=True)
class Order(ABC):
    order_id: str
    user: User
    restaurant: Restaurant
    items: List[MenuItem]
    price_calculator: PriceCalculator
    payment_strategy: PaymentStrategy
    delivery_method: DeliveryMethod
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    scheduled_for: Optional[datetime] = None
    payment_receipt: Optional[str] = None

    def total_price(self) -> float:
        return self.price_calculator.calc_total(self.items)

    def delivery_type(self) -> str:
        return self.delivery_method.get_type()

    def pay(self) -> str:
        receipt = self.payment_strategy.pay(self.total_price())
        self.payment_receipt = receipt
        return receipt

    def summary(self) -> str:
        return (
            f"Order({self.order_id}) user={self.user.user_id} "
            f"restaurant={self.restaurant.restaurant_id} "
            f"items={len(self.items)} total={self.total_price():.2f} "
            f"type={self.delivery_type()} scheduled_for={self.scheduled_for}"
        )


@dataclass(slots=True)
class NowOrder(Order):
    pass


@dataclass(slots=True)
class ScheduledOrder(Order):
    def __post_init__(self) -> None:
        if self.scheduled_for is None:
            raise ValueError("ScheduledOrder requires scheduled_for")


def validate_items_belong_to_restaurant(items: Sequence[MenuItem], restaurant: Restaurant) -> None:
    menu_ids = {i.item_id for i in restaurant.menu_items}
    for item in items:
        if item.item_id not in menu_ids:
            raise ValueError(f"Item {item.item_id} is not in restaurant menu")

