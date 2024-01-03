import math

import numpy as np

rnd = np.random
rnd.seed(0)


class Passenger:
    """
    Passenger class

    This class contains paramiters and action sets of the passenger agent.

    Intended Usage: If you are making changes here you are changing either the data pertaining to the passenger agent or
    their action set.

    TODO Action sets

    :param id: Passenger Id
    :type id: int

    :param xcord: Passenger Coordinate on the X axis
    :type xcord: int

    :param ycord: Passenger Coordinate on the Y axis
    :type ycord: int

    :param destination_x: Coordinates of the passenger destination on the X axis
    :type destination_x: int

    :param destination_y: Coordinates of the passenger destination on the Y axis
    :type destination_y: int

    :param capacity_cost: Passenger capacity cost, standard passenger is 1 wheelchair is 4 ect
    :type capacity_cost: int

    :param walk_cost: The cost to have the passenger move 1 unit [Note, currently an arbitrary value]
    :type walk_cost: int

    :param speed: Rate at witch the passengers move
    :type speed: int

    :param pickup_time: Target pickup time
    :type pickup_time: int

    :param dropoff_time: Target time the passenger wants to get to their destination
    :type droproff_time: int

    :param booked: If the passenger has booked in advance
    :type booked: bool

    :param lateness: How much overall time the passenger will allow for lateness
    :type lateness: int
    """

    def __init__(self, id, xcord, ycord, destination_x, destination_y, capacity_cost, walk_cost, speed,
                 pickup_time, dropoff_time, booked, lateness):
        """Constructor method"""
        self.id = id
        self.lat = xcord
        self.long = ycord
        self.destination_x = destination_x
        self.destination_y = destination_y
        self.capacity_cost = capacity_cost
        self.walk_cost = walk_cost
        self.speed = speed
        self.pickup_time = pickup_time
        self.dropoff_time = dropoff_time
        self.booked = booked
        self.lateness = lateness
        self.journey_start_time = rnd.randint(1, self.pickup_time)
        if self.booked:
            self.booking_time = 0

    def getNearestStop(self, stop_list):
        """
        Get the nearest stop to the passenger from the stops contained in the stop_list

        :param stop_list: List of eligible stops
        :type stop_list: List of <Stops>

        :return: The nearest stop to the passenger
        :rtype: Stop
        """
        current_nearest = stop_list[0]
        for s in stop_list:
            if self.calcDistance(self.lat, self.long, s.lat, s.long) < \
                    self.calcDistance(self.lat, self.long, current_nearest.lat, current_nearest.long):
                current_nearest = s

        return current_nearest

    def getNearestDrop(self, stop_list):
        """
            Get the nearest stop to the passengers destination from the stops contained in the stop_list

            :param stop_list: List of eligible stops
            :type stop_list: List of Stops

            :return: The nearest stop to the passenger destination
            :rtype: Stop
        """

        current_nearest = stop_list[0]
        for s in stop_list:
            if self.calcDistance(self.destination_x, self.destination_y, s.lat, s.long) < \
                    self.calcDistance(self.destination_x, self.destination_y, current_nearest.lat,
                                      current_nearest.long):
                current_nearest = s

        return current_nearest

    def calcTimeToTravel(self, x1, y1, x2, y2):
        """
        Return the time it will take the passenger to move between two points

        :param x1: Passenger X cord
        :type x1: int

        :param y1: Passenger Y cord
        :type y1: int

        :param x2: Destination X cord
        :type x2: int

        :param y2: Destination Y cord
        :type y2: int

        :return: Time to travel
        :rtype: int
        """
        return self.calcDistance(x1, y1, x2, y2) / self.speed

    def calcDistance(self, x1, y1, x2, y2):
        """
            Return the distance between two points

            :param x1: First X cord
            :type x1: int

            :param y1: First Y cord
            :type y1: int

            :param x2: Second X cord
            :type x2: int

            :param y2: Second Y cord
            :type y2: int

            :return: Distance between two points
            :rtype: int
        """
        return math.sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)

    def set_booking_time(self, value):
        """
        Set the time that the booking is made

        :param value: Time the booking is made
        :type value: int

        """

        self.booking_time = value

    def get_booking_time(self):
        """
        Get the time that the booking is made
        :return: The booking time
        :rtype: int
        """

        return self.booking_time
