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
        self.total_time = 0
        self.total_distance = 0

    def getStartStopId(self):
        """Returns the id of the starting stop
        :return: Returns the stop ID of the buses starting stop
        :rtype: int
        """
        return self.start_stop.getStopId()
    
    def increase_total_time(self, value):
        """
        Increase the total time the bus has been on the route

        :param value: Time to increase by
        :type value: int
        """
        self.total_time += value
        
    def increase_total_distance(self, value):
        """
        Increase the total distance the bus has been on the route

        :param value: Distance to increase by
        :type value: int
        """
        self.total_distance += value
        
    def get_total_time(self):
        """
        Get the total time the bus has been on the route

        :return: Total time the bus has been on the route
        :rtype: int
        """
        return self.total_time

    def get_total_distance(self):
        """
        Get the total distance the bus has been on the route

        :return: Total distance the bus has been on the route
        :rtype: int
        """
        return self.total_distance
