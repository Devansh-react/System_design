from __future__ import annotations


class Car:
    def __init__(self) -> None:
        self.speed = 0

    def accelerate(self) -> None:
        print("Accelerating")
        self.speed += 20

    # Postcondition: speed must reduce after brake
    def brake(self) -> None:
        print("Applying brakes")
        self.speed -= 20


class HybridCar(Car):
    def __init__(self) -> None:
        super().__init__()
        self.charge = 0

    # Strengthened postcondition:
    # - speed reduces
    # - charge increases
    def brake(self) -> None:
        print("Applying brakes")
        self.speed -= 20
        self.charge += 10


def main() -> None:
    car: Car = HybridCar()
    car.brake()  # Works fine: speed reduces and also increases charge


if __name__ == "__main__":
    main()

