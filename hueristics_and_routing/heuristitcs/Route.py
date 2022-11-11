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

    def __init__(self, stop, arrival_time, wait_time, passenger_manifest):
        """Constructor method"""
        self.stop = stop
        self.arrival_time = arrival_time
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
        :rtype: int
        """
        return self.arrival_time

    def getWait(self):
        """
        :return: Vehicle wait time
        :rtype: int
        """
        return self.wait_time