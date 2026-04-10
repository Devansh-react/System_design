from __future__ import annotations

from dataclasses import dataclass

from food_delivery.models.order import Order


@dataclass(slots=True)
class NotificationService:
    channel: str = "console"

    def notify_order_placed(self, order: Order) -> None:
        # Replace with Email/SMS/Push integrations later.
        print(f"[NOTIFY:{self.channel}] Order placed: {order.summary()}")

