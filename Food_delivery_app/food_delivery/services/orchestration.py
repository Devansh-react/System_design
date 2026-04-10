from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from food_delivery.factories.order_factory import OrderFactory
from food_delivery.managers.order_manager import OrderManager
from food_delivery.managers.restaurant_manager import RestaurantManager
from food_delivery.models.menu_item import MenuItem
from food_delivery.models.order import Order
from food_delivery.models.restaurant import Restaurant
from food_delivery.models.user import User
from food_delivery.services.notification import NotificationService
from food_delivery.strategies.delivery import DeliveryMethod
from food_delivery.strategies.payment import PaymentStrategy
from food_delivery.strategies.pricing import PriceCalculator


@dataclass(slots=True)
class FoodDeliverySystem:
    restaurant_manager: RestaurantManager = field(default_factory=RestaurantManager)
    order_manager: OrderManager = field(default_factory=OrderManager)
    order_factory: OrderFactory = field(default_factory=OrderFactory)
    notifier: NotificationService = field(default_factory=NotificationService)

    def search_restaurants(self, *, user: User) -> List[Restaurant]:
        return self.restaurant_manager.search_by_location(user.location)

    def place_order_from_cart(
        self,
        *,
        user: User,
        restaurant: Restaurant,
        price_calculator: PriceCalculator,
        payment_strategy: PaymentStrategy,
        delivery_method: DeliveryMethod,
        order_type: str = "now",
        scheduled_for: Optional[datetime] = None,
    ) -> Order:
        items: List[MenuItem] = user.cart.as_menu_items_expanded()
        if not items:
            raise ValueError("Cart is empty")

        order = self.order_factory.create_order(
            order_type=order_type,
            user=user,
            restaurant=restaurant,
            items=items,
            price_calculator=price_calculator,
            payment_strategy=payment_strategy,
            delivery_method=delivery_method,
            scheduled_for=scheduled_for,
        )

        order.pay()
        self.order_manager.add_order(order)
        self.order_manager.save_to_db()
        self.notifier.notify_order_placed(order)
        user.cart.clear()
        return order

