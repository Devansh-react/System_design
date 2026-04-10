from __future__ import annotations

from abc import ABC, abstractmethod


class DeliveryMethod(ABC):
    @abstractmethod
    def get_type(self) -> str: ...


class PickupMethod(DeliveryMethod):
    def get_type(self) -> str:
        return "PICKUP"


class HomeDeliveryMethod(DeliveryMethod):
    def get_type(self) -> str:
        return "DELIVERY"

