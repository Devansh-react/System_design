ef park_vehicle(self, vehicle: Vehicle) -> Optional[Ticket]:
        for floor in self.floors:
            spot = floor.find_and_park(vehicle)
            if spot:
                return Ticket(vehicle, s