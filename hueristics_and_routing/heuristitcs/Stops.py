import math
import numpy as np


class Stop:
    """
        A class that handles the parameters of the stops, generally all these parameters are taken from the parameters that
        are taken from the XML flags in the `Open Street Map <https://www.openstreetmap.org/>`_ data. These flags make this
        class very cumbersome. However, these details will be integral to integrating the accessibility into the system.
        Additionally many of these flags are null in the OSM data, this is an issue with the data source and future
        data collection will cover these flags.

        :param id: Stop id
        :type id: int

        :param name: The name of the bus stop or street
        :type name: str

        :param lat: Latitude coordinate
        :type lat: Float

        :param long: Longitude coordinate
        :type long: Float

        :param local_ref: Unofficial name
        :type local_ref: str

        :param network: Bus network stop belongs too
        :type network: str

        :param operator: Who operates the stop
        :type operator: str

        :param shelter: Is there a bus shelter present
        :type shelter: bool

        :param bench: Is there a bench present
        :type bench: bool

        :param tactile_paving: Is tactile paving present
        :type tactile_paving: bool

        :param wheelchair: Is the stop wheelchair accessible
        :type wheelchair: bool

        :param departure_board: Is there are live departure board at the stop
        :type departure_board: bool

        :param lit: Are there streetlights present
        :type lit: bool

        :param bins: Are there bins at the stop
        :type bins: bool

        :param covered: Is there a cover from rain at the stop
        :type covered: bool

        :param passenger_information_display: Is there a dynamic information board present
        :type passenger_information_display: bool

        :param pole: Is there a pole with bus information
        :type pole: bool

        :param flag: Is there a stop flag present
        :type flag: bool

        :param kerb: Is there a dropped kerb at the stop
        :type kerb: bool

        :param traffic_sign: Is there a traffic sign at the stop
        :type traffic_sign: bool

        :param advertising: Is there an advertisement at the stop
        :type advertising: bool

        :param layer: The height layer the stop is on
        :type layer: int

        :param street: The street name
        :type street: str

        :param crossing: The name of the nearest crossing
        :type crossing: str

        :param look_up_index: The stops position in the lookup table
        :type look_up_index: int
    """

    def __init__(self, id, name, lat, long, local_ref, network, operator, shelter, bench, tactile_paving, wheelchair,
                 departure_board, lit, bins, covered, passenger_information_display, pole, flag, kerb, traffic_sign,
                 advertising, layer, street, crossing, look_up_index):
        """Constructor method"""
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
        """
            :return: The stop ID
            :rtype: int
        """
        return self.id

    def getNearStop(self, stop_list):
        """
            :param stop_list: List of valid stops to check
            :type stop_list: List of <Stops>

            :return: Nearest stop to the stop from the list of valid stops
            :rtype: Stop
        """
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
        """
        :param stop_list: List of valid stops to check
        :type stop_list: List of <Stops>

        :return: Random stop from list
        :rtype: Stop
        """
        return np.random.choice(list(stop_list))

