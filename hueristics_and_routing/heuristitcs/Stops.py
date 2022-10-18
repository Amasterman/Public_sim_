import math
import numpy as np


class Stop:

    def __init__(self, id, name, lat, long, local_ref, network, operator, shelter, bench, tactile_paving, wheelchair,
                 departure_board, lit, bins, covered, passenger_information_display, pole, flag, kerb, traffic_sign,
                 advertising, layer, street, crossing, look_up_index):
        self.id = id
        self.name = name
        self.lat = float(lat)
        self.long = float(long)
        self.local_ref = local_ref
        self.network = network
        self.operator = operator
        self.shelter = shelter
        self.bench = bench
        self.tactile_paving = tactile_paving
        self.wheelchair = wheelchair
        self.departure_board = departure_board
        self.lit = lit
        self.bins = bins
        self.covered = covered
        self.passenger_information_display = passenger_information_display
        self.pole = pole
        self.flag = flag
        self.kerb = kerb
        self.traffic_sign = traffic_sign
        self.advertising = advertising
        self.layer = layer
        self.street = street
        self.crossing = crossing
        self.look_up_index = look_up_index

    def getStopId(self):
        return self.id

    def getNearStop(self, stop_list):
        to_list = list(stop_list)
        current_nearest = None
        if bool(to_list):
            current_nearest = to_list[0]

            for s in to_list:
                if self.calcDistance(self.lat, self.long, s.lat, s.long) < self.calcDistance(self.lat,
                                                                                                   self.long,
                                                                                                   current_nearest.lat,
                                                                                                   current_nearest.long):
                    current_nearest = s

        return current_nearest

    def getRandStop(self, stop_list):

        return np.random.choice(list(stop_list))

    def calcDistance(self, x1, y1, x2, y2):
        return math.sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)


