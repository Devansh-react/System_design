from __future__ import annotations


class LogicError(Exception):
    pass


class OutOfRange(LogicError):
    pass


class Parent:
    # Parent throws LogicError
    def get_value(self) -> None:
        raise LogicError("Parent error")


class Child(Parent):
    # Child throws a narrower exception (subclass of LogicError)
    def get_value(self) -> None:
        raise OutOfRange("Child error")
        # Raising RuntimeError here would be "broader" vs LogicError in spirit.


class Client:
    def __init__(self, p: Parent) -> None:
        self.p = p

    def take_value(self) -> None:
        try:
            self.p.get_value()
        except LogicError as e:
            print(f"Logic error exception occured : {e}")


def main() -> None:
    parent = Parent()
    child = Child()

    client = Client(parent)
    # client = Client(child)
    client.take_value()


if __name__ == "__main__":
    main()

