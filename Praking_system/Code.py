import math
import threading
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum
from itertools import count
from typing import List, Optional


# ===================== ENUMS =====================
class VehicleType(Enum):
    BIKE = 1
    CAR = 2
    TRUCK = 3


class TicketStatus(Enum):
    ACTIVE = 1
    PAID = 2


class PaymentStatus(Enum):
    SUCCESS = 1
    FAILED = 2


# ===================== VEHICLES + FACTORY =====================
class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.type = vehicle_type


class Car(Vehicle):
    def __init__(self, plate):
        super().__init__(plate, VehicleType.CAR)


class Bike(Vehicle):
    def __init__(self, plate):
        super().__init__(plate, VehicleType.BIKE)


class Truck(Vehicle):
    def __init__(self, plate):
        super().__init__(plate, VehicleType.TRUCK)


class VehicleFactory:
    @staticmethod
    def create(vehicle_type: VehicleType, plate: str) -> Vehicle:
        mapping = {
            VehicleType.BIKE: Bike,
            VehicleType.CAR: Car,
            VehicleType.TRUCK: Truck,
        }
        return mapping[vehicle_type](plate)


# ===================== SPOT + FLOOR =====================
class ParkingSpot:
    def __init__(self, spot_id: int, spot_type: VehicleType):
        self.id = spot_id
        self.spot_type = spot_type
        self.vehicle: Optional[Vehicle] = None
        self._occupied = False
        self._lock = threading.Lock()  # one lock PER spot, not for the whole lot

    def is_free(self) -> bool:
        return not self._occupied

    def can_fit(self, vehicle: Vehicle) -> bool:
        return self.spot_type == vehicle.type

    def try_park(self, vehicle: Vehicle) -> bool:
        # Atomic check-and-set: only ONE thread can flip False -> True
        with self._lock:
            if self._occupied:
                return False
            self._occupied = True
            self.vehicle = vehicle
            return True

    def unpark(self) -> None:
        with self._lock:
            self._occupied = False
            self.vehicle = None


class ParkingFloor:
    def __init__(self, floor_number: int, spots: List[ParkingSpot]):
        self.floor_number = floor_number
        self.spots = spots

    def find_and_park(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        for spot in self.spots:
            if spot.can_fit(vehicle) and spot.try_park(vehicle):
                return spot
        return None


# ===================== TICKET =====================
class Ticket:
    _ids = count(1)

    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_id = next(Ticket._ids)
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.now()
        self.exit_time: Optional[datetime] = None
        self.status = TicketStatus.ACTIVE


# ===================== PRICING (STRATEGY) =====================
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, ticket: Ticket) -> float:
        pass


class TimeBasedPricing(PricingStrategy):
    HOURLY_RATE = {VehicleType.BIKE: 10, VehicleType.CAR: 20, VehicleType.TRUCK: 40}

    def calculate_fee(self, ticket: Ticket) -> float:
        minutes = (ticket.exit_time - ticket.entry_time).total_seconds() / 60
        hours = max(1, math.ceil(minutes / 60))  # round up, min 1 hour
        return hours * self.HOURLY_RATE[ticket.vehicle.type]


class EventBasedPricing(PricingStrategy):
    FLAT_FEE = {VehicleType.BIKE: 50, VehicleType.CAR: 100, VehicleType.TRUCK: 200}

    def calculate_fee(self, ticket: Ticket) -> float:
        return self.FLAT_FEE[ticket.vehicle.type]


# ===================== PAYMENT (STRATEGY) =====================
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass


class CardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"  Paid {amount} by CARD")
        return True


class UpiPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"  Paid {amount} by UPI")
        return True


class CashPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"  Paid {amount} by CASH")
        return True


class Payment:
    def __init__(self, ticket_id: int, amount: float, status: PaymentStatus):
        self.ticket_id = ticket_id
        self.amount = amount
        self.status = status


class PaymentProcessor:
    def process(self, ticket_id: int, amount: float, strategy: PaymentStrategy) -> Payment:
        ok = strategy.pay(amount)
        return Payment(ticket_id, amount, PaymentStatus.SUCCESS if ok else PaymentStatus.FAILED)


# ===================== PARKING LOT (SINGLETON) =====================
class ParkingLot:
    _instance = None

    @classmethod
    def get_instance(cls, floors, entry_count, exit_count, pricing):
        if cls._instance is None:
            cls._instance = ParkingLot(floors, entry_count, exit_count, pricing)
        return cls._instance

    # floors and gate counts are passed in -> "dynamic" requirement
    def __init__(self, floors: List[ParkingFloor], entry_count: int, exit_count: int,
                 pricing: PricingStrategy):
        self.floors = floors
        self.pricing_strategy = pricing
        self.entry_gates = [EntryGate(i, self) for i in range(1, entry_count + 1)]
        self.exit_gates = [ExitGate(i, self) for i in range(1, exit_count + 1)]

    def set_pricing_strategy(self, pricing: PricingStrategy) -> None:
        self.pricing_strategy = pricing

    def park_vehicle(self, vehicle: Vehicle) -> Optional[Ticket]:
        for floor in self.floors:
            spot = floor.find_and_park(vehicle)
            if spot:
                return Ticket(vehicle, spot)
        return None  # lot full for this vehicle type

    def unpark_vehicle(self, ticket: Ticket) -> None:
        ticket.spot.unpark()
        ticket.status = TicketStatus.PAID


# ===================== GATES =====================
class Gate(ABC):
    def __init__(self, gate_id: int, lot: ParkingLot):
        self.gate_id = gate_id
        self.lot = lot


class EntryGate(Gate):
    def generate_ticket(self, vehicle: Vehicle) -> Optional[Ticket]:
        ticket = self.lot.park_vehicle(vehicle)
        if ticket is None:
            print(f"  Entry gate {self.gate_id}: NO SPOT for {vehicle.license_plate}")
        return ticket


class ExitGate(Gate):
    def __init__(self, gate_id: int, lot: ParkingLot):
        super().__init__(gate_id, lot)
        self.payment_processor = PaymentProcessor()

    def process_exit(self, ticket: Ticket, payment_strategy: PaymentStrategy) -> bool:
        ticket.exit_time = datetime.now()
        fee = self.lot.pricing_strategy.calculate_fee(ticket)
        payment = self.payment_processor.process(ticket.ticket_id, fee, payment_strategy)

        if payment.status == PaymentStatus.SUCCESS:
            self.lot.unpark_vehicle(ticket)  # free the spot ONLY after payment succeeds
            return True
        return False


# ===================== DEMO =====================
if __name__ == "__main__":
    # 2 floors, each: 1 bike spot, 2 car spots, 1 truck spot
    floors = []
    spot_id = 1
    for f in range(1, 3):
        spots = []
        for t in (VehicleType.BIKE, VehicleType.CAR, VehicleType.CAR, VehicleType.TRUCK):
            spots.append(ParkingSpot(spot_id, t))
            spot_id += 1
        floors.append(ParkingFloor(f, spots))

    lot = ParkingLot.get_instance(floors, 2, 2, TimeBasedPricing())
    entry = lot.entry_gates[0]
    exit_gate = lot.exit_gates[0]

    # ---- Test 1: normal entry and exit (time based) ----
    print("Test 1: Car, time based pricing")
    t1 = entry.generate_ticket(VehicleFactory.create(VehicleType.CAR, "RJ14-1234"))
    print(f"  Ticket {t1.ticket_id} -> spot {t1.spot.id}")
    t1.entry_time = datetime.now() - timedelta(hours=2, minutes=10)  # pretend 2h10m ago -> 3 hours
    exit_gate.process_exit(t1, UpiPayment())
    print(f"  Ticket status: {t1.status.name}, spot free: {t1.spot.is_free()}")

    # ---- Test 2: switch to event based pricing ----
    print("\nTest 2: Bike, event based pricing")
    lot.set_pricing_strategy(EventBasedPricing())
    t2 = entry.generate_ticket(VehicleFactory.create(VehicleType.BIKE, "RJ14-0001"))
    exit_gate.process_exit(t2, CashPayment())

    # ---- Test 3: lot full for a vehicle type ----
    print("\nTest 3: Only 2 truck spots exist, 3rd truck must fail")
    entry.generate_ticket(VehicleFactory.create(VehicleType.TRUCK, "T-1"))
    entry.generate_ticket(VehicleFactory.create(VehicleType.TRUCK, "T-2"))
    t3 = entry.generate_ticket(VehicleFactory.create(VehicleType.TRUCK, "T-3"))
    print(f"  3rd truck ticket is None? {t3 is None}")

    # ---- Test 4: concurrency - 5 bikes race for 1 bike spot ----
    print("\nTest 4: Concurrency, 5 bikes race for 1 bike spot")
    race_floor = ParkingFloor(1, [ParkingSpot(100, VehicleType.BIKE)])
    results = []

    def try_park(n):
        bike = VehicleFactory.create(VehicleType.BIKE, f"RACE-{n}")
        results.append(race_floor.find_and_park(bike) is not None)  # list.append is thread-safe

    threads = [threading.Thread(target=try_park, args=(i,)) for i in range(5)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    print(f"  Bikes parked in the 1 spot: {sum(results)} (expected 1)")