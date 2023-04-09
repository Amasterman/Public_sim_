import math

import numpy as np
from math import radians, sin, cos, sqrt, atan2

rnd = np.random
rnd.seed(0)


class Passenger:
    """
    Passenger class

    This class contains all the information regarding the passenger, it is currently a WIP as the data from the surveys
    have not been implemented. Currently the class contians the id, start coords, destination coords, capacity cost,
    walk_cost, speed, target pick up time, dropoff time, weather or not they are booked in advance and the maximum
    allowable lateness.

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
        self.origin_x = xcord
        self.origin_y = ycord
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
        self.first_stop = 0,
        self.total_time = 0
        self.total_distance=0
        
        self.should_walk = False

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
            if self.calc_distance(self.lat, self.long, s.lat, s.long) < \
                    self.calc_distance(self.lat, self.long, current_nearest.lat, current_nearest.long):
                current_nearest = s
    
        return current_nearest
    
    # when the nearest stop has a big impact on the total bus travel time or distance
    def getOptimalNearest(self,stop_list,exclude_stops):
        """
        Get the nearest stop to the passenger from the stops contained in the stop_list that are different from the ones in the excluded_stops list

        :param stop_list: List of eligible stops
        :type stop_list: List of <Stops>
        
        :param exlude_stops: List of stops to exclude
        :type exlude_stops: List of <Stops>

        :return: The nearest stop to the passenger
        :rtype: Stop
        """
        
        current_nearest = stop_list[0]
        for s in stop_list:
            if s not in exclude_stops:
                if self.calc_distance(self.lat, self.long, s.lat, s.long) < \
                        self.calc_distance(self.lat, self.long, current_nearest.lat, current_nearest.long):
                    current_nearest = s
      
        return current_nearest
        
    
    def shouldWalkToDestination(self, stop_list):
        current_nearest = self.getNearestStop(stop_list)
        if(self.calc_distance(self.lat, self.long, self.destination_x, self.destination_y) < \
                self.calc_distance(self.lat, self.long, current_nearest.lat, current_nearest.long)):
            print (self.id, "walking to destination")
            self.should_walk = True
            return True
        return False

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
            if self.calc_distance(self.destination_x, self.destination_y, s.lat, s.long) < \
                    self.calc_distance(self.destination_x, self.destination_y, current_nearest.lat,
                                      current_nearest.long):
                current_nearest = s
        return current_nearest

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
    
    def increase_total_time(self, value):
        """
        Increase the total time the passenger has been on the bus

        :param value: Time to increase by
        :type value: int
        """

        self.total_time += value
        
    def increase_total_distance(self, value):
        """
        Increase the total distance the passenger has been on the bus

        :param value: Distance to increase by
        :type value: int
        """

        self.total_distance += value
        
    # Set the passengers current position lat and long
    def set_current_pos(self, lat, long):
        """
        Set the passengers latitude

        :param value: Latitude
        :type value: int
        """

        self.lat = lat
        self.long = long
        
    def get_current_pos(self):
        """
        Get the passengers current position

        :return: The passengers current position
        :rtype: int
        """

        return self.lat, self.long
        
    def get_total_time(self):
        """
        Get the total time the passenger has been on the bus
        :return: Total time
        :rtype: int
        """

        return self.total_time
    
    def get_total_distance(self):
        """
        Get the total distance the passenger has been on the bus
        :return: Total distance
        :rtype: int
        """

        return self.total_distance  
    
    def calc_distance(self,lat1, lon1, lat2, lon2):
        R = 6371  # Radius of the Earth in kilometers

         # Convert latitude and longitude to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
        # Calculate the differences in latitude and longitude
        dlat = lat2 - lat1
        dlon = lon2 - lon1
    
        # Calculate the Haversine formula
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        d = R * c * 1000  # Distance in meters

        return d