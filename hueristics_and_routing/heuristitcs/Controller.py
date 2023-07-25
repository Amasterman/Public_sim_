import itertools


class Controller:
    """
    This Class acts as the overall manager for the simulator, taking user input and data files and serving them to the
    correct heuristic solver as well as managing the world enviornment inputs. The overall aim is to create a flexible
    framework that manages the janker parts of the sim.

    Intended use: In general if you are tweaking this you are aiming to change what
    data is being served to various parts of the sim, not changing how that data is generated.

    """

    def __init__(self, no_buses, no_passengers, max_bus_cap, max_lateness, sim_runs):
        """Constructor method"""
        # Seed settings. Here we have two seeds, one for sim randomization and one for heuristic randomization

        # Sim randomization
        self.rnd_sim = np.random
        self.rnd_sim_seed = 1
        self.rnd_sim.seed(self.rnd_sim_seed)

        # Heuristic randomization
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
        # TODO Replace ths random selector with the data set information,
        #  might need to still need to have some randomness as there are multiple depos on the map
        self.depo = list_of_stops[rnd_sim.randint(0, no_stops)]

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
    def generate_booking_times(self, passengers):
        # booking times can appear either at the moment they want to be picked up or a percentage in advance (lets start
        # with 30%?

        roll_preeminence = 0
        roll_prebook = 0

        passenger_preeminence_percent = 50
        passenger_prebook_percentage = .30

        for passenger in passengers:
            roll_preeminence = random(0, 100)
            if roll_preeminence < passenger_preeminence_percent:
                passenger.set_booking_time(passenger.pickup_time)
            else:
                roll_prebook = random(0, passenger_prebook_percentage, 0.01)
                passenger.set_booking_time(passenger.pickup_time * (1 + roll_prebook))

        return passenger

    def import_stop_data(self):
        # Stop importer; IN XML scraped from www.openstreetmap.org OUT List of stop objects
        # Open file with CSV reader
        with open("XML_to_CSV_OUT.CSV", newline='') as csvfile:
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
        self.no_stops = len(list_of_stops)

    def import_stop_relations_data(self):
        # Initialze the psudo-array
        for i in range(0, no_stops):
            self.stop_relations.append([])
            for j in range(0, no_stops):
                self.stop_relations[i].append("")

        # Reset temp variables
        i = 0
        j = 0

        # Open file generated by ProjectOSM
        with open("route_durations.CSV", newline='') as csvfile:
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

    def generate_buses(self):
        # Random bus generator
        # TODO Need to get some more info on the buses in the area, unilink and bluestar maybe?
        for i in range(0, self.no_buses):
            # Generate vehicle with random parameters, also potential to be renamed
            temp_bus = Bus.Buses(i, depo, rnd_sim.randint(4, max_bus_cap), rnd_sim.randint(30, 70),
                                 rnd_sim.randint(1, 4), depo)

            # Append to list
            self.list_of_buses.append(temp_bus)

    def generate_passenger(self):
        # Two versions for static and dynamic versions. Decided by the preivously declared global variable.
        if dynamic:
            # Generate up to the target number of passengers
            for i in range(0, self.no_passengers):
                # Generate random passenger data including if the trip has been booked in advance
                temp_passenger = Pass.Passenger(i, rnd_sim.uniform(minlat, maxlat), rnd_sim.uniform(minlon, maxlon),
                                                rnd_sim.uniform(minlat, maxlat),
                                                rnd_sim.uniform(minlon, maxlon), rnd_sim.randint(1, 4), rnd_sim.randint(1, 100),
                                                rnd_sim.randint(1, 3), rnd_sim.randint(1, 1000), rnd_sim.randint(2000, 10000),
                                                bool(random.getrandbits(1)), max_lateness)

                # Append to list of passengers
                self.list_of_passengers.append(temp_passenger)
        else:
            # Generate random passenger data the prebooked flag is set to 1
            for i in range(0, self.no_passengers):
                temp_passenger = Pass.Passenger(i, rnd_sim.uniform(minlat, maxlat), rnd_sim.uniform(minlon, maxlon),
                                                rnd_sim.uniform(minlat, maxlat),
                                                rnd_sim.uniform(minlon, maxlon), rnd_sim.randint(1, 4), rnd_sim.randint(1, 100),
                                                rnd_sim.randint(1, 3), rnd_sim.randint(1, 1000), rnd_sim.randint(2000, 10000), 1,
                                                max_lateness)

                # Append to list of passengers
                self.list_of_passengers.append(temp_passenger)

    # Tick up sim seed
    def inc_sim_seed(self):
        self.rnd_sim_seed += 1

    # Tick up heuristic seed
    def inc_heur_seed(self):
        self.rnd_hur_seed += 1

    # Tick up both
    def inc_both_seeds(self):
        self.inc_sim_seed()
        self.inc_heur_seed()

    def inti_all(self, passengers):
        self.import_stop_data()
        self.import_stop_relations_data()
        self.generate_passenger()
        self.generate_buses()

        # This may be wrong
        self.list_of_passengers = self.generate_booking_times(self.list_of_passengers)


    # ------------------------------------------------------------------------------------Route heirstics and Validation

