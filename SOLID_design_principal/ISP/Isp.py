from __future__ import annotations

from abc import ABC, abstractmethod


class TwoDimensionalShape(ABC):
    @abstractmethod
    def area(self) -> float:
        raise NotImplementedError


class ThreeDimensionalShape(ABC):
    @abstractmethod
    def area(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def volume(self) -> float:
        raise NotImplementedError


class Square(TwoDimensionalShape):
    def __init__(self, side: float) -> None:
        self._side = side

    def area(self) -> float:
        return self._side * self._side


class Rectangle(TwoDimensionalShape):
    def __init__(self, length: float, width: float) -> None:
        self._length = length
        self._width = width

    def area(self) -> float:
        return self._length * self._width


class Cube(ThreeDimensionalShape):
    def __init__(self, side: float) -> None:
        self._side = side

    def area(self) -> float:
        return 6 * self._side * self._side

    def volume(self) -> float:
        return self._side * self._side * self._side


def main() -> None:
    square: TwoDimensionalShape = Square(5)
    rectangle: TwoDimensionalShape = Rectangle(4, 6)
    cube: ThreeDimensionalShape = Cube(3)

    print(f"Square Area: {square.area()}")
    print(f"Rectangle Area: {rectangle.area()}")
    print(f"Cube Area: {cube.area()}")
    print(f"Cube Volume: {cube.volume()}")


if __name__ == "__main__":
    main()

