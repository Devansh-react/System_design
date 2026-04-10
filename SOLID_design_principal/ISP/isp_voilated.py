from __future__ import annotations

from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def volume(self) -> float:
        raise NotImplementedError


class Square(Shape):
    def __init__(self, side: float) -> None:
        self._side = side

    def area(self) -> float:
        return self._side * self._side

    def volume(self) -> float:
        raise ValueError("Volume not applicable for Square")


class Rectangle(Shape):
    def __init__(self, length: float, width: float) -> None:
        self._length = length
        self._width = width

    def area(self) -> float:
        return self._length * self._width

    def volume(self) -> float:
        raise ValueError("Volume not applicable for Rectangle")


class Cube(Shape):
    def __init__(self, side: float) -> None:
        self._side = side

    def area(self) -> float:
        return 6 * self._side * self._side

    def volume(self) -> float:
        return self._side * self._side * self._side


def main() -> None:
    square: Shape = Square(5)
    rectangle: Shape = Rectangle(4, 6)
    cube: Shape = Cube(3)

    print(f"Square Area: {square.area()}")
    print(f"Rectangle Area: {rectangle.area()}")
    print(f"Cube Area: {cube.area()}")
    print(f"Cube Volume: {cube.volume()}")

    try:
        print(f"Square Volume: {square.volume()}")
    except ValueError as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()

