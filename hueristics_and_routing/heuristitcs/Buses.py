class Buses:
    """Class for the buses

    This includes the id, start stop, bus capacity, speed and running cost.
    TODO Include ownership and accessibility
    """

    def __init__(self, id, start_stop, bus_capacity, speed, running_cost, current_stop):
        self.id = id
        self.start_stop = start_stop
        self.bus_capacity = bus_capacity
        self.speed = speed
        self.running_cost = running_cost
        self.current_stop = start_stop

    def getStartStopId(self):
        """Returns the id of the starting stop"""
        return self.start_stop.getStopId()