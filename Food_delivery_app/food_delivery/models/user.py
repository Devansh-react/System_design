from __future__ import annotations

from dataclasses import dataclass, field

from food_delivery.models.cart import Cart


@dataclass(slots=True)
class User:
    user_id: str
    name: str
    location: str
    email: str
    cart: Cart = field(default_factory=Cart)

