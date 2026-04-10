from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from food_delivery.models.menu_item import MenuItem
from food_delivery.models.order import NowOrder, ScheduledOrder, validate_items_belong_to_restaurant
from food_delivery.models.restaurant import Restaurant
from food_delivery.models.user import User
from food_delivery.strategies.delivery import DeliveryMethod
from food_delivery.strategies.payment import PaymentStrategy
from food_delivery.strategies.pricing import PriceCalculator


@dataclass(slots=True)
class OrderFactory:
    prefix: str = "ord_"

    def create_order(
        self,
        *,
        order_type: str,
        user: User,
        restaurant: Restaurant,
        items: List[MenuItem],
        price_calculator: PriceCalculator,
        payment_strategy: PaymentStrategy,
        delivery_method: DeliveryMethod,
        scheduled_for: Optional[datetime] = None,
    ):
        validate_items_belong_to_restaurant(items, restaurant)
        oid = f"{self.prefix}{uuid4().hex[:10]}"
        t = order_type.strip().lower()
        if t in {"now", "order_now", "instant"}:
            return NowOrder(
                order_id=oid,
                user=user,
                restaurant=restaurant,
                items=list(items),
                price_calculator=price_calculator,
                payment_strategy=payment_strategy,
                delivery_method=delivery_method,
            )
        if t in {"scheduled", "schedule", "schedule_order"}:
            return ScheduledOrder(
                order_id=oid,
                user=user,
                restaurant=restaurant,
                items=list(items),
                price_calculator=price_calculator,
                payment_strategy=payment_strategy,
                delivery_method=delivery_method,
                scheduled_for=scheduled_for,
            )
        raise ValueError(f"Unknown order_type: {order_type}")

