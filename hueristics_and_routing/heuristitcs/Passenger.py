import math

import numpy as np

rnd = np.random
rnd.seed(0)


class Passenger:
    """"Passenger class, this ones a bit of a dosey

    This class contains all the information regarding the passenger, it is currently a WIP as the data from the surveys
    have not been implemented. Currently the class contians the id, start coords, destination coords, capacity cost,
    walk_cost, speed, target pick up time, dropoff time, weather or not they are booked in advance and the maximum
    allowable lateness.
    """

    def __init__(self, id, xcord, ycord, destination_x, destination_y, capacity_cost, walk_cost, speed,
                 pickup_time, dropoff_time, booked, lateness):
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
        current_nearest = stop_list[0]
        for s in stop_list:
            if self.calcDistance(self.lat, self.long, s.lat, s.long) < \
                    self.calcDistance(self.lat, self.long, current_nearest.lat, current_nearest.long):
                current_nearest = s

        return current_nearest

    def getNearestDrop(self, stop_list):

        current_nearest = stop_list[0]
        for s in stop_list:
            if self.calcDistance(self.destination_x, self.destination_y, s.lat, s.long) < \
                    self.calcDistance(self.destination_x, self.destination_y, current_nearest.lat,
                                      current_nearest.long):
                current_nearest = s

        return current_nearest

    def calcTimeToTravel(self, x1, y1, x2, y2):
        return self.calcDistance(x1, y1, x2, y2) / self.speed

    def calcDistance(self, x1, y1, x2, y2):
        return math.sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)

    def set_booking_time(self, value):
        self.booking_time = value

    def get_booking_time(self):
        return self.booking_time