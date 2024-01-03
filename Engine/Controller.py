import csv

import numpy as np

import Stops as Stop
from Agents.Transtportation_Agents import Buses as Bus
import Passenger as Pass


class Controller:
    """
    This Class acts as the overall manager for the simulator, taking user input and data files and serving them to the
    correct heuristic solver as well as managing the world enviornment inputs. The overall aim is to create a flexible
    framework that manages the janker parts of the sim.

    Intended use: In general if you are tweaking this you are aiming to change what
    data is being served to various parts of the sim, not changing how that data is generated.

    :param no_buses: How many bus agents are used in the simulator
    :type no_buses: int

    :param no_passengers: How many passenger agents are used in the simulator
    :type no_passengers: int

    :param max_bus_cap: The maximum amount of passengers a bus can hold
    :type max_bus_cap: int

    :param max_lateness: The maximum time a passenger will allow the bus to be late before canceling
    :type max_lateness: int

    :param sim_runs: How many runs of the sim will be run
    :type sim_runs: int
    """

    def __init__(self, no_buses, no_passengers, max_bus_cap, max_lateness, sim_runs):
        """Constructor method"""
        # Seed settings. Here we have two seeds, one for sim randomization and one for heuristic randomization

        # Sim randomization
        self.rnd_sim = np.random
        self.rnd_sim_seed = 1
        self.rnd_sim.seed(self.rnd_sim_seed)

        # Heuristics randomization
        self.rnd_hur = np.random
        self.rnd_hur_seed = 20
        self.rnd_hur.seed(self.rnd_hur_seed)

        # Global toggle for dynamism [UI setting?]
        self.dynamic = False

        # Passenger bookings in advance within a dynamic system
        self.passenger_bookings = []

        # Area of longitude and latitude of the greater Southampton area [Better way to define?]
        self.minlat = 50.8255000
        self.minlon = -1.6263000
        self.maxlat = 51.0142000
        self.maxlon = -1.0873000

        # Amount of Buses
        self.no_buses = no_buses
        # Amount of passengers
        self.no_passengers = no_passengers

        # Bus max capacity
        self.max_bus_cap = max_bus_cap

        # List of stop locations
        self.list_of_stops = []

        # Init blank no of stops
        self.no_stops = 0

        # Psudo-array of time between stops. Indexed in MxM
        self.stop_relations = []

        # List of vehicles, could be renamed in future to reflect the diffrent vehicles
        self.list_of_buses = []

        # Depo is the start and stop position of the buses
        self.depo = None

        # List of passengers
        self.list_of_passengers = []

        # Max tolerable time difference between targeted arrival and actual arrival
        self.max_lateness = max_lateness

        # Two lists; passengers booked more than a day in advance/repeat trips, and new requests
        self.passenger_booked = []
        self.passenger_not_booked = []

        # Testing settings
        self.sim_runs = sim_runs

    # -------------------------------------------------------------------------------------Initialization and generators
    def generate_booking_times(self, passengers, preeminence_percent, preebook_percent):
        """
        Generator for the the booking time paramiter. By passing the population (or a sample) of passengers it will set
        a percentage (set by passenger_preeminence_precent) of the passengers to be random passengers where their pickup
        time is the same as their booking time, or passengers who have prebooked and ie their pickup time exists after
        their booking time.

        :param passengers: The population of passengers that you want to set as booked/nonbooked
        :type passengers: List<passengers>

        :param preeminence_percent: The percentage of passengers who have prebooked
        :type preeminence_percent: int

        :param preebook_percent: The maximum percantage of pickup time in advance that the passenger booked
        :type preebook_percent: float

        :return: passengers
        :rtype: List<Passengers>
        """

        roll_preeminence = 0
        roll_prebook = 0

        passenger_preeminence_percent = preeminence_percent
        passenger_prebook_percentage = preebook_percent

        for passenger in passengers:
            roll_preeminence = self.rnd_sim.rand(0, 100)
            if roll_preeminence < passenger_preeminence_percent:
                passenger.set_booking_time(passenger.pickup_time)
                passenger.booked = 0
            else:
                roll_prebook = self.rnd_sim.rand(0, passenger_prebook_percentage, 0.01)
                passenger.set_booking_time(passenger.pickup_time - (passenger.pickup_time * roll_prebook))
                passenger.booked = 1

        return passengers

    def import_stop_data(self):
        """
        Runs the stop importer to extract the stop data from the CSV to the self.list_of_stops
        """

        # Stop importer; IN XML scraped from www.openstreetmap.org OUT List of stop objects
        # Open file with CSV reader
        with open("../Files/Out/XML_to_CSV_OUT.CSV", newline='') as csvfile:
            # Skip header line
            next(csvfile)

            # Break count will limit the amount of stops imported. << means all included
            break_count = 50000
            count = 0

            # Begin reading the CSV using the "," as a separator (Note the XML scraper sanitizes the inputs)
            for row in csvfile:
                row = row.split(',')

                # Creates a stop object using the rows as parameters. Currently very inflexible.
                temp_stop = Stop.Stop(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                      row[10],
                                      row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19],
                                      row[20],
                                      row[21], row[22], row[23], count)

                # Append stop to list of stops
                self.list_of_stops.append(temp_stop)

                # Keep track of the count and break if break count met
                count = count + 1
                if break_count == count:
                    break

        # Close the CSV writer
        csvfile.close()

        # count list entries
        self.no_stops = len(self.list_of_stops)

    def import_stop_relations_data(self):
        """
        Extracts the relationship data between stops (read time between) from the ProjectOSM generated file into an
        array. This array is implicitly indexed by the X Y position in the array corresponding to the stop in the same
        position in self.list_of_stops

        """
        # Initialize the array
        for i in range(0, self.no_stops):
            self.stop_relations.append([])
            for j in range(0, self.no_stops):
                self.stop_relations[i].append("")

        # Reset temp variables
        i = 0
        j = 0

        # Open file generated by ProjectOSM
        with open("../Files/Out/route_durations.CSV", newline='') as csvfile:
            # for row in csvfile:
            # row = row.split(',')
            # j = 0
            # for elements in row:
            #  stop_relations[i][j] = elements
            #   j += 1
            # i += 1

            # Set up reader to read directly from file into an array
            reader = csv.reader(csvfile)
            rows = list(reader)
            for g in range(0, self.no_stops):
                for f in range(0, self.no_stops):
                    self.stop_relations[g][f] = rows[g][f]

    def generate_depo(self, stops):
        """
        Randomly selects a stop from the provided list of stops to be the designated depo
        """
        self.depo = stops[self.rnd_sim.randint(0, len(stops))]

    def generate_buses(self):
        """
        Generate the parameters and list of the bus agents.

        """

        for i in range(0, self.no_buses):
            # Generate vehicle with random parameters, also potential to be renamed
            temp_bus = Bus.Buses(i, self.depo, self.rnd_sim.randint(4, self.max_bus_cap), self.rnd_sim.randint(30, 70),
                                 self.rnd_sim.randint(1, 4), self.depo)

            # Append to list
            self.list_of_buses.append(temp_bus)

    def generate_passenger(self):
        """
        Generate the parameters and list of passenger agents
        """
        # Generate random passenger data the prebooked flag is set to 1
        for i in range(0, self.no_passengers):
            temp_passenger = Pass.Passenger(i, self.rnd_sim.uniform(self.minlat, self.maxlat),
                                            self.rnd_sim.uniform(self.minlon, self.maxlon),
                                            self.rnd_sim.uniform(self.minlat, self.maxlat),
                                            self.rnd_sim.uniform(self.minlon, self.maxlon), self.rnd_sim.randint(1, 4),
                                            self.rnd_sim.randint(1, 100),
                                            self.rnd_sim.randint(1, 3), self.rnd_sim.randint(1, 1000),
                                            self.rnd_sim.randint(2000, 10000), 1,
                                            self.max_lateness)

            # Append to list of passengers
            self.list_of_passengers.append(temp_passenger)

    # Tick up sim seed
    def inc_sim_seed(self):
        """
        Increment Simulator seed
        """

        self.rnd_sim_seed += 1

    # Tick up heuristic seed
    def inc_heur_seed(self):
        """
        Increment Heuristics seed
        """
        self.rnd_hur_seed += 1

    # Tick up both
    def inc_both_seeds(self):
        """
        Increment both sim and hur seeds
        """
        self.inc_sim_seed()
        self.inc_heur_seed()

    def inti_all_gen(self, passengers):
        """
        This will initialize and run all the generators needed to initialize the world settings
        """
        self.import_stop_data()
        self.import_stop_relations_data()
        self.generate_depo(self.list_of_stops)
        self.generate_passenger()
        self.generate_buses()

        # The preeminance and preebook need to be made more versatile
        self.list_of_passengers = self.generate_booking_times(self.list_of_passengers, 50, 0.5)

    # ------------------------------------------------------------------------------------Route heirstics and Validation
