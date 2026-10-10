from typing import List, Set
from enum import Enum
from abc import ABC, abstractmethod


class Direction(Enum):
    UP = 1
    DOWN = 2
    IDLE = 3


class DoorStatus(Enum):
    OPEN = 1
    CLOSED = 2


class DirectionRequest(Enum):
    PICK_UP = 1
    PICK_DOWN = 2
    DESTINATION = 3


# Backward-compatible alias for the original naming.
Direction_request = DirectionRequest


class Request:
    # Hall call request; destination request inside elevator.
    def __init__(self, floor: int, direction: DirectionRequest):
        self._floor = floor
        self._direction = direction

    def get_floor(self) -> int:
        return self._floor

    def get_req_type(self) -> DirectionRequest:
        return self._direction


request = Request


class Elevator(ABC):
    def __init__(self, id: int, floor: int = 0, direction: Direction = Direction.IDLE):
        self.id = id
        self.floor = floor
        self.direction = direction
        self.stops: List[int] = []
        self.door_status = DoorStatus.CLOSED
        self.request_queue: Set[Request] = set()

    def add_request(self, request: Request) -> bool:
        self.request_queue.add(request)
        return True

    def get_current_direction(self) -> Direction:
        return self.direction

    def get_current_floor(self) -> int:
        return self.floor

    def has_requests_in_current_direction(self) -> bool:
        if self.direction == Direction.UP:
            return any(request.get_floor() > self.floor for request in self.request_queue)
        if self.direction == Direction.DOWN:
            return any(request.get_floor() < self.floor for request in self.request_queue)
        return bool(self.request_queue)

    def step(self) -> None:
        if not self.request_queue:
            self.direction = Direction.IDLE
            return

        if self.direction == Direction.IDLE:
            nearest_request = min(self.request_queue, key=lambda r: abs(r.get_floor() - self.floor))
            if nearest_request.get_floor() > self.floor:
                self.direction = Direction.UP
            else:
                self.direction = Direction.DOWN

        if any(request.get_floor() == self.floor for request in self.request_queue):
            self.door_status = DoorStatus.OPEN
            self.request_queue = {
                request
                for request in self.request_queue
                if request.get_floor() != self.floor
            }
            if not self.has_requests_in_current_direction():
                self.direction = Direction.DOWN if self.direction == Direction.UP else Direction.UP
            return

        if not self.has_requests_in_current_direction():
            self.direction = Direction.DOWN if self.direction == Direction.UP else Direction.UP

        if self.direction == Direction.UP:
            self.floor += 1
        elif self.direction == Direction.DOWN:
            self.floor -= 1


class Elevator_Controller:
    def __init__(self):
        self.elevators: List[Elevator] = []

    def step(self) -> None:
        for e in self.elevators:
            e.step()

    def  find_elevator(self, floor: int, direction: Direction_request):
        def Moving_towards(self, floor: int, direction: Direction_request):
            min_distance = 1e9
            best_elevator = None
            for elevator in self.elevators:
                current_floor = elevator.get_current_floor()
                moving_in_requested_direction = (
                    (direction == DirectionRequest.PICK_UP and elevator.get_current_direction() == Direction.UP and current_floor <= floor)
                    or (direction == DirectionRequest.PICK_DOWN and elevator.get_current_direction() == Direction.DOWN and current_floor >= floor)
                )
                if moving_in_requested_direction and abs(current_floor - floor) < min_distance:
                    min_distance = abs(current_floor - floor)
                    best_elevator = elevator
            return best_elevator
        def idle_elevator(self,floor: int, direction: Direction_request):
                    min_distance=1e9
                    best_elevator = None
                    for elevator in self.elevators:
                        if elevator.get_current_direction() == Direction.IDLE:
                            if abs(elevator.get_current_floor()-self.floor)<min_distance:
                                min_distance = abs(elevator.get_current_floor()-self.floor)
                                best_elevator = elevator
                    return best_elevator
        def nearest_elevator(self,floor: int, direction: Direction_request):
                    min_distance=1e9
                    best_elevator = None
                    for elevator in self.elevators:
                        if abs(elevator.get_current_floor-self.floor)<min_distance:
                            min_distance = abs(elevator.get_current_floor()-self.floor)
                            best_elevator = elevator
                    return best_elevator

        cat1  = Moving_towards(self,floor,direction)
        if cat1 is not None:
            return cat1
        cat2 = idle_elevator(self,floor,direction)
        if cat2 is not None:
            return cat2
        cat3 = nearest_elevator(self,floor,direction)
        if cat3 is not None:
            return cat3
        
        request = Request(floor, direction)
        best_elevator = cat3
        if best_elevator is None:
            return None
        return best_elevator.add_request(request)
    
        
        
        
        