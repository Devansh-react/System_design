from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Product:
    name: str
    price: float


class ShoppingCart:
    def __init__(self) -> None:
        self._products: List[Product] = []

    def add_product(self, product: Product) -> None:
        self._products.append(product)

    def get_products(self) -> List[Product]:
        return list(self._products)

    def calculate_total(self) -> float:
        return sum(p.price for p in self._products)


class ShoppingCartPrinter:
    def __init__(self, cart: ShoppingCart) -> None:
        self._cart = cart

    def print_invoice(self) -> None:
        print("Shopping Cart Invoice:")
        for p in self._cart.get_products():
            print(f"{p.name} - Rs {p.price}")
        print(f"Total: Rs {self._cart.calculate_total()}")


class ShoppingCartStorage:
    """
    Violating OCP: to add a new storage type you must MODIFY this class
    (by adding another save_to_* method).
    """

    def __init__(self, cart: ShoppingCart) -> None:
        self._cart = cart

    def save_to_sql_database(self) -> None:
        _ = self._cart
        print("Saving shopping cart to SQL DB...")

    def save_to_mongo_database(self) -> None:
        _ = self._cart
        print("Saving shopping cart to Mongo DB...")

    def save_to_file(self) -> None:
        _ = self._cart
        print("Saving shopping cart to File...")


def main() -> None:
    cart = ShoppingCart()
    cart.add_product(Product("Laptop", 50000))
    cart.add_product(Product("Mouse", 2000))

    printer = ShoppingCartPrinter(cart)
    printer.print_invoice()

    storage = ShoppingCartStorage(cart)
    storage.save_to_file()


if __name__ == "__main__":
    main()

