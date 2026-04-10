from __future__ import annotations


class Parent:
    def print(self, msg: str) -> None:
        print(f"Parent: {msg}")


class Child(Parent):
    def print(self, msg: str) -> None:
        print(f"Child: {msg}")


class Client:
    def __init__(self, p: Parent) -> None:
        self.p = p

    def print_msg(self) -> None:
        self.p.print("Hello")


def main() -> None:
    parent = Parent()
    child: Parent = Child()

    # client = Client(parent)
    client = Client(child)
    client.print_msg()


if __name__ == "__main__":
    main()

