from __future__ import annotations

from typing import Protocol


class Animal:
    pass


class Dog(Animal):
    pass


class Parent:
    def get_animal(self) -> Animal:
        print("Parent : Returning Animal instance")
        return Animal()


class Child(Parent):
    # Covariant return type: returning a subtype (Dog) is OK
    def get_animal(self) -> Dog:
        print("Child : Returning Dog instance")
        return Dog()


class ParentLike(Protocol):
    def get_animal(self) -> Animal: ...


class Client:
    def __init__(self, p: ParentLike) -> None:
        self.p = p

    def take_animal(self) -> None:
        self.p.get_animal()


def main() -> None:
    parent = Parent()
    child = Child()

    client = Client(child)
    # client = Client(parent)
    client.take_animal()


if __name__ == "__main__":
    main()

