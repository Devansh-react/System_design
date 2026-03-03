from abc import ABC, abstractmethod


# Product 1 --> Burger
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


class BasicWheatBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Basic Wheat Burger with bun, patty, and ketchup!")


class StandardWheatBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Standard Wheat Burger with bun, patty, cheese, and lettuce!")


class PremiumWheatBurger(Burger):
    def prepare(self) -> None:
        print(
            "Preparing Premium Wheat Burger with gourmet bun, premium patty, "
            "cheese, lettuce, and secret sauce!"
        )


# Product 2 --> GarlicBread
class GarlicBread(ABC):
    @abstractmethod
    def prepare(self) -> None:
        pass


class BasicGarlicBread(GarlicBread):
    def prepare(self) -> None:
        print("Preparing Basic Garlic Bread with butter and garlic!")


class CheeseGarlicBread(GarlicBread):
    def prepare(self) -> None:
        print("Preparing Cheese Garlic Bread with extra cheese and butter!")


class BasicWheatGarlicBread(GarlicBread):
    def prepare(self) -> None:
        print("Preparing Basic Wheat Garlic Bread with butter and garlic!")


class CheeseWheatGarlicBread(GarlicBread):
    def prepare(self) -> None:
        print("Preparing Cheese Wheat Garlic Bread with extra cheese and butter!")


# Factory and its concretions
class MealFactory(ABC):
    @abstractmethod
    def create_burger(self, burger_type: str) -> Burger | None:
        pass

    @abstractmethod
    def create_garlic_bread(self, garlic_type: str) -> GarlicBread | None:
        pass


class SinghBurger(MealFactory):
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

    def create_garlic_bread(self, garlic_type: str) -> GarlicBread | None:
        garlic_type = garlic_type.lower()
        if garlic_type == "basic":
            return BasicGarlicBread()
        elif garlic_type == "cheese":
            return CheeseGarlicBread()
        else:
            print("Invalid Garlic bread type!")
            return None


class KingBurger(MealFactory):
    def create_burger(self, burger_type: str) -> Burger | None:
        burger_type = burger_type.lower()
        if burger_type == "basic":
            return BasicWheatBurger()
        elif burger_type == "standard":
            return StandardWheatBurger()
        elif burger_type == "premium":
            return PremiumWheatBurger()
        else:
            print("Invalid burger type!")
            return None

    def create_garlic_bread(self, garlic_type: str) -> GarlicBread | None:
        garlic_type = garlic_type.lower()
        if garlic_type == "basic":
            return BasicWheatGarlicBread()
        elif garlic_type == "cheese":
            return CheeseWheatGarlicBread()
        else:
            print("Invalid Garlic bread type!")
            return None


if __name__ == "__main__":
    burger_type = "basic"
    garlic_bread_type = "cheese"

    meal_factory: MealFactory = KingBurger()

    burger = meal_factory.create_burger(burger_type)
    garlic_bread = meal_factory.create_garlic_bread(garlic_bread_type)

    if burger is not None:
        burger.prepare()
    if garlic_bread is not None:
        garlic_bread.prepare()