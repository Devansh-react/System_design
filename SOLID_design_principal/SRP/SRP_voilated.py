from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Product:
    name: str
    price: float


class ShoppingCart:
    """
    Violating SRP: ShoppingCart handles cart logic + printing + persistence.
    """

    def __init__(self) -> None:
        self._products: List[Product] = []

    def add_product(self, product: Product) -> None:
        self._products.append(product)

    def get_products(self) -> List[Product]:
        return list(self._products)

    def calculate_total(self) -> float:
        return sum(p.price for p in self._products)

    # Violating SRP - printing concern
    def print_invoice(self) -> None:
        print("Shopping Cart Invoice:")
        for p in self._products:
            print(f"{p.name} - Rs {p.price}")
        print(f"Total: Rs {self.calculate_total()}")

    # Violating SRP - persistence concern
    def save_to_database(self) -> None:
        print("Saving shopping cart to database...")


def main() -> None:
    cart = ShoppingCart()
    cart.add_product(Product("Laptop", 50000))
    cart.add_product(Product("Mouse", 2000))

    cart.print_invoice()
    cart.save_to_database()


if __name__ == "__main__":
    main()

