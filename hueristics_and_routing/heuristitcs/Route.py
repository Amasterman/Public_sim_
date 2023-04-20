class Route:
    """
    Class contains information for a section of the route, contains the information about passengers and timing info

    :param stop: The stop that is relevant to the route section
    :type stop: Stop

    :param arrival_time: The time the vehicle arrives at the stop
    :type arrival_time: int

    :param wait_time: The time the vehicle is waiting at the stop
    :type wait_time: int

    :param passenger_manifest: List of passengers on vehicle at the stop
    :type passenger_manifest: List of <Passengers>

    """

    def __init__(self, stop, set_off , arrival_time,distance, wait_time, passenger_manifest):
        """Constructor method"""
        self.stop = stop
        self.set_off = set_off
        self.arrival_time = arrival_time
        self.distance = distance
        self.wait_time = wait_time
        self.passenger_manifest = passenger_manifest

    def getPassengers(self):
        """
        :return: List of passengers
        :rtype: List of <passengers>
        """
        return self.passenger_manifest

    def getStops(self):
        """
        :return: Get the Stop the vehicle is at
        :rtype: Stop
        """
        return self.stop

    def getArrival(self):
        """
        :return: Get the arrival time of the vehicle
        :rtype: Datetime
        """
        return self.arrival_time

    def getWait(self):
        """
        :return: Vehicle wait time
        :rtype: int
        """
        return self.wait_time
    
    def getDistance(self):
        """
        :return: Distance travelled
        :rtype: int
        """
        return self.distance
    
    def getSetOff(self):
        """
        :return: Time the vehicle leaves the stop
        :rtype: Datetime
        """
        return self.set_off