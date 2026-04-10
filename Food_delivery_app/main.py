from __future__ import annotations

from datetime import UTC, datetime, timedelta

from food_delivery.managers.restaurant_manager import RestaurantManager
from food_delivery.models.menu_item import MenuItem
from food_delivery.models.restaurant import Restaurant
from food_delivery.models.user import User
from food_delivery.services.orchestration import FoodDeliverySystem
from food_delivery.strategies.delivery import HomeDeliveryMethod, PickupMethod
from food_delivery.strategies.payment import CardPayment, NetBankingPayment, UpiPayment
from food_delivery.strategies.pricing import SimplePriceCalculator


def seed_restaurants(rm: RestaurantManager) -> None:
    r1 = Restaurant(
        restaurant_id="res_1",
        name="Spice Hub",
        address="12 MG Road",
        location="Bangalore",
    )
    r1.add_menu_item(MenuItem(item_id="itm_1", name="Paneer Tikka", price=180.0))
    r1.add_menu_item(MenuItem(item_id="itm_2", name="Butter Naan", price=45.0))

    r2 = Restaurant(
        restaurant_id="res_2",
        name="Pizza Point",
        address="77 Church Street",
        location="Bangalore",
    )
    r2.add_menu_item(MenuItem(item_id="itm_3", name="Margherita", price=250.0))
    r2.add_menu_item(MenuItem(item_id="itm_4", name="Coke", price=60.0))

    rm.create(r1)
    rm.create(r2)


def demo_now_order() -> None:
    system = FoodDeliverySystem()
    seed_restaurants(system.restaurant_manager)

    user = User(user_id="usr_1", name="Asha", location="Bangalore", email="asha@example.com")
    restaurants = system.search_restaurants(user=user)
    restaurant = restaurants[0]

    user.cart.add_item(restaurant.menu_items[0], qty=1)
    user.cart.add_item(restaurant.menu_items[1], qty=2)

    price_calc = SimplePriceCalculator(delivery_fee=30.0, tax_rate=0.05)
    payment = UpiPayment("asha@upi")
    delivery = HomeDeliveryMethod()

    order = system.place_order_from_cart(
        user=user,
        restaurant=restaurant,
        price_calculator=price_calc,
        payment_strategy=payment,
        delivery_method=delivery,
        order_type="now",
    )
    print(order.summary())


def demo_scheduled_pickup() -> None:
    system = FoodDeliverySystem()
    # singleton managers keep state across system instances
    user = User(user_id="usr_2", name="Rohit", location="Bangalore", email="rohit@example.com")

    restaurant = system.restaurant_manager.get("res_2")
    if restaurant is None:
        seed_restaurants(system.restaurant_manager)
        restaurant = system.restaurant_manager.get("res_2")
        assert restaurant is not None

    user.cart.add_item(restaurant.menu_items[0], qty=1)
    user.cart.add_item(restaurant.menu_items[1], qty=1)

    price_calc = SimplePriceCalculator(delivery_fee=0.0, tax_rate=0.02)
    payment = CardPayment("1234")
    delivery = PickupMethod()

    order = system.place_order_from_cart(
        user=user,
        restaurant=restaurant,
        price_calculator=price_calc,
        payment_strategy=payment,
        delivery_method=delivery,
        order_type="scheduled",
        scheduled_for=datetime.now(UTC) + timedelta(hours=2),
    )
    print(order.summary())


if __name__ == "__main__":
    demo_now_order()
    demo_scheduled_pickup()

