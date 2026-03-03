from abc import ABC, abstractmethod


class Burger(ABC):
    @abstractmethod
    def prepare(self) -> None:
        pass


class BasicBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Basic Burger with bun, patty, and ketchup!")


class StandardBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Standard Burger with bun, patty, cheese, and lettuce!")


class PremiumBurger(Burger):
    def prepare(self) -> None:
        print(
            "Preparing Premium Burger with gourmet bun, premium patty, "
            "cheese, lettuce, and secret sauce!"
        )


class BurgerFactory:
    def create_burger(self, burger_type: str) -> Burger | None:
        burger_type = burger_type.lower()
        if burger_type == "basic":
            return BasicBurger()
        elif burger_type == "standard":
            return StandardBurger()
        elif burger_type == "premium":
            return PremiumBurger()
        else:
            print("Invalid burger type!")
            return None


if __name__ == "__main__":
    burger_type = "standard"

    my_burger_factory = BurgerFactory()
    burger = my_burger_factory.create_burger(burger_type)

    if burger is not None:
        burger.prepare()