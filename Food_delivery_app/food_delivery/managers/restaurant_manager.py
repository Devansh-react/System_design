from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from food_delivery.models.restaurant import Restaurant
from food_delivery.utils.singleton import SingletonMeta


@dataclass
class RestaurantManager(metaclass=SingletonMeta):
    _restaurants: Dict[str, Restaurant] = field(default_factory=dict)

    def create(self, restaurant: Restaurant) -> None:
        if restaurant.restaurant_id in self._restaurants:
            raise ValueError(f"Restaurant already exists: {restaurant.restaurant_id}")
        self._restaurants[restaurant.restaurant_id] = restaurant

    def get(self, restaurant_id: str) -> Optional[Restaurant]:
        return self._restaurants.get(restaurant_id)

    def update(self, restaurant: Restaurant) -> None:
        if restaurant.restaurant_id not in self._restaurants:
            raise KeyError(f"Restaurant not found: {restaurant.restaurant_id}")
        self._restaurants[restaurant.restaurant_id] = restaurant

    def delete(self, restaurant_id: str) -> None:
        self._restaurants.pop(restaurant_id, None)

    def list_all(self) -> List[Restaurant]:
        return list(self._restaurants.values())

    def search_by_location(self, location: str) -> List[Restaurant]:
        loc = location.strip().lower()
        return [r for r in self._restaurants.values() if r.location.strip().lower() == loc]

