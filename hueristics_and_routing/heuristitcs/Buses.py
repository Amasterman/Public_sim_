class Buses:
    """
    Class containing the details of buses

    :param id: ID of the bus
    :type id: int

    :param start_stop: The stop the bus begins its journey at
    :type start_stop: Stop

    :param bus_capacity: Maximum passenger capacity
    :type bus_capacity: int

    :param speed: Speed the bus travels
    :type speed: int

    :param running_cost: The cost of moving the bus a single unit
    :type running_cost: int

    :param  current_stop: The current stop the bus is at
    :type current_stop: Stop

    TODO Include ownership and accessibility
    """

    def __init__(self, id, start_stop, bus_capacity, speed, running_cost, current_stop):
        """Constructor method"""
        self.id = id
        self.start_stop = start_stop
        self.bus_capacity = bus_capacity
        self.speed = speed
        self.running_cost = running_cost
        self.current_stop = start_stop

    def getStartStopId(self):
        """Returns the id of the starting stop
        :return: Returns the stop ID of the buses starting stop
        :rtype: int
        """
        return self.start_stop.getStopId()
