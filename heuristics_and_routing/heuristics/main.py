# Initial setup
import math
import time

import csv

import matplotlib.pyplot as plt
import numpy as np

import Buses as Bus
import Passenger as Pass
import Route as Route
import Stops as Stop

# -----------------------  Random settings
cntr_rnd = np.random
cntr_rnd.seed(1)

heur_rnd = np.random
heur_rnd.seed(2)
# -----------------------  World settings

# Global toggle for dynamism [UI setting?]
dynamic = False

# Passenger bookings in advance within a dynamic system
passenger_bookings = []

# Area of longitude and latitude of the greater Southampton area [Better way to define?]
minlat = 50.8255000
minlon = -1.6263000
maxlat = 51.0142000
maxlon = -1.0873000

# Amount of Buses
no_buses = 5
# Amount of passengers
no_passengers = 30

# Bus max capacity
max_bus_cap = 15

# Set of stops
# = [i for i in range(0, no_stops)]
# Set of busses
# B = [i for i in range(0, no_buses)]

# Dont know why this is still here
# maxPad = 1000

# -----------------------  Stop settings

# List of stop locations
list_of_stops = []

# Stop importer; IN XML scraped from www.openstreetmap.org OUT List of stop objects
# Open file with CSV reader
with open("XML_to_CSV_OUT.CSV", newline='') as csvfile:
    # Skip header line
    next(csvfile)

    # Break count will limit the amount of stops imported. << means all included
    break_count = 5000
    count = 0

    # Begin reading the CSV using the "," as a separator (Note the XML scraper sanitizes the inputs)
    for row in csvfile:
        row = row.split(',')

        # Creates a stop object using the rows as parameters. Currently very inflexible.
        temp_stop = Stop.Stop(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                              row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20],
                              row[21], row[22], row[23], count)

        # Append stop to list of stops
        list_of_stops.append(temp_stop)

        # Keep track of the count and break if break count met
        count = count + 1
        if break_count == count:
            break

# Close the CSV writer
csvfile.close()

# count list entries
no_stops = len(list_of_stops)

# -----------------------  Stop relations

# Psudo-array of time between stops. Indexed in MxM
stop_relations = []

# Initialze the psudo-array
for i in range(0, no_stops):
    stop_relations.append([])
    for j in range(0, no_stops):
        stop_relations[i].append("")

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
    for g in range(0, no_stops):
        for f in range(0, no_stops):
            stop_relations[g][f] = rows[g][f]

# -----------------------  Bus settings

# List of vehicles, could be renamed in future to reflect the diffrent vehicles
list_of_buses = []

# Depo is the start and stop position of the buses
# TODO Replace ths random selector with the data set information,
#  might need to still need to have some randomness as there are multiple depos on the map
depo = list_of_stops[cntr_rnd.randint(0, no_stops)]

# Random bus generator
# TODO Need to get some more info on the buses in the area, unilink and bluestar maybe?
for i in range(0, no_buses):
    # Generate vehicle with random parameters, also potential to be renamed
    temp_bus = Bus.Buses(i, depo, cntr_rnd.randint(4, max_bus_cap), cntr_rnd.randint(30, 70),
                         cntr_rnd.randint(1, 4), depo)

    # Append to list
    list_of_buses.append(temp_bus)

# -----------------------  Passenger settings

# List of passengers
list_of_passengers = []

# TODO All of this is subject to change, this data is kinda unknowable until the surveys are complete

# Max tolerable time difference between targeted arrival and actual arrival
max_lateness = 1000

# Two versions for static and dynamic versions. Decided by the preivously declared global variable.
if dynamic:
    # Generate up to the target number of passengers
    for i in range(0, no_passengers):
        # Generate random passenger data including if the trip has been booked in advance
        temp_passenger = Pass.Passenger(i, cntr_rnd.uniform(minlat, maxlat), cntr_rnd.uniform(minlon, maxlon),
                                        cntr_rnd.uniform(minlat, maxlat),
                                        cntr_rnd.uniform(minlon, maxlon), cntr_rnd.randint(1, 4),
                                        cntr_rnd.randint(1, 100),
                                        cntr_rnd.randint(1, 3), cntr_rnd.randint(1, 1000),
                                        cntr_rnd.randint(2000, 10000),
                                        bool(random.getrandbits(1)), max_lateness)

        # Append to list of passengers
        list_of_passengers.append(temp_passenger)
else:
    # Generate random passenger data the prebooked flag is set to 1
    for i in range(0, no_passengers):
        temp_passenger = Pass.Passenger(i, cntr_rnd.uniform(minlat, maxlat), cntr_rnd.uniform(minlon, maxlon),
                                        cntr_rnd.uniform(minlat, maxlat),
                                        cntr_rnd.uniform(minlon, maxlon), cntr_rnd.randint(1, 4),
                                        cntr_rnd.randint(1, 100),
                                        cntr_rnd.randint(1, 3), cntr_rnd.randint(1, 1000),
                                        cntr_rnd.randint(2000, 10000), 1,
                                        max_lateness)

        # Append to list of passengers
        list_of_passengers.append(temp_passenger)

# ----------------------- Ant Colony settings

# Time metric for the algorithm
simTime = 0

# alpha and beta hyper parameters for tuning
a_hyp = 2
b_hyp = 2

# Stinky bois smell rate (Pheromone drop amount)
Q_const = 1

# Pheromone trails
pheromone_trails = []

# Initialize the pheromone trial pseudo-array with very high values (May need to increase not sure)
for i in range(0, no_stops):
    pheromone_trails.append([])
    for j in range(0, no_stops):
        pheromone_trails[i].append(2000)

# Stop probabilities stop_probs[bus,stop,stop]
stop_probs = []

# Initialise the stop probabilities pseudo-array
for b in range(0, no_buses):
    stop_probs.append([])
    for i in range(0, no_stops):
        stop_probs[b].append([])
        for j in range(0, no_stops):
            stop_probs[b][i].append(np.longdouble(0))

# ----------------------- Dynamic setup

# Two lists; passengers booked more than a day in advance/repeat trips, and new requests
passenger_booked = []
passenger_not_booked = []

# ----------------------- Consensus Setup

# Delta Hyper parameter nbOpt lookahead steps
delta = 10

# nbOpt time, From the offline variant
nbOpt = 10

# d as found in the literature
d = 10

# Schedule as defined in the literature
schedule = None

# ---------------------- Passenger grouping

# passenger influence range in coord ranges? Dunno how thats gonna pan out
passenger_influence_range = 0.2


# run the system on the provided method and time the time it takes to run
def run(method):
    # Take the computer time before the run
    start_time = time.perf_counter()

    # Dived the selection by dynamic and static
    if dynamic:
        # Init Dynamic
        int_dynamic()

        # Switch statement for selecting the heuristic
        # Ok no switch statment thats in python 3.10 and im not updatitng and breaking everything again
        if method == "greedy":
            return greedy_online()

        elif method == "ant":
            return ant_colony_online()

        elif method == "consensus":
            return concensus_online()
        pass

    else:

        # Init Static
        list_of_active_stops, passenger_bookings = ini_static()

        # Switch statement for selecting the heuristic
        if method == "greedy":
            return greedy_offline(list_of_active_stops, passenger_bookings)

        elif method == "ant":
            return ant_colony(list_of_active_stops)

        elif method == "consensus":
            return consensus()

        pass

    # Take the differance between the start time and the current clock time to get the run time
    run_time = time.perf_counter() - start_time
    print("Method " + method + " finished in " + str(run_time))


def int_dynamic():
    # Check through passengers for those who have booked in advance vs appear
    # Populate the the lists based on the booked value
    for i in range(0, no_passengers):
        if list_of_passengers[i].booked:
            passenger_booked.append(list_of_passengers[i])
        else:
            passenger_not_booked.append(list_of_passengers[i])

    # The dynamically appearing passengers need a time to appear
    generate_booking_times(passenger_not_booked)


def serve_new_booking(current_time, active_passengers):
    temp_new_passenger = []

    # Iterate through the non booked passengers and serve any passengers that have arrived in the time that have not
    for passenger in passenger_not_booked:
        if passenger not in active_passengers and passenger.booking_time() < current_time:
            temp_new_passenger.append(passenger)

    return temp_new_passenger


def ini_static():
    for i in range(0, no_passengers):
        if list_of_passengers[i].booked:
            passenger_booked.append(list_of_passengers[i])

    # Retrieve the stops that have a passenger waiting and add start and stops to the booking register
    list_of_active_stops, passenger_bookings = user_stops()

    return list_of_active_stops, passenger_bookings

def generate_booking_times(passengers):
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


# The offline (ie non dynamic) version of the greedy heuristic
# TODO Improve implementation of the heuristic
def greedy_offline(list_of_active_stops, passenger_bookings):
    return route_generator(list_of_passengers.copy(), list_of_buses.copy(), list_of_active_stops, depo)


# Return all stops in use for this set of passengers and the booking register
def user_stops():
    # Get the Greedy nearest pick and drop stops
    # TODO improve this away from a greedy method
    for p in passenger_booked:
        passenger_bookings.append([p.getNearestStop(list_of_stops), p.getNearestDrop(list_of_stops)])

    # Initialize an empty set
    list_of_active_stops = set()

    # Take start stop elements from passenger bookings and add to the list of active stops
    for elements in passenger_bookings:
        one, two = elements
        if one not in list_of_active_stops:
            list_of_active_stops.add(one)
    # if two not in list_of_active_stops:
    #     list_of_active_stops.add(two)

    # Convert set to list
    list_of_active_stops = list(list_of_active_stops)

    # Return list and bookings
    return list_of_active_stops, passenger_bookings


# Validate the passed routes, validation includes route connections, passenger pick up, drop off and bus capacity
# TODO validate the validation on the real data set
def validate_route(passenger_route, bus_route):
    # List of passenger target arrival time, indexed by position
    passenger_stop_arrival = []

    # Save passenger stop arrival time indexed by passenger location
    for p in passenger_booked:
        passenger_stop_arrival.append(p.journey_start_time + p.calcTimeToTravel(p.lat, p.long,
                                                                                passenger_route[p.id][0].lat,
                                                                                passenger_route[p.id][0].long))

    # Check each bus validity
    for bus in range(0, len(bus_route)):

        # Store current bus
        current_bus = bus_route[bus]
        stop_order = []
        passenger_manifest = []
        passengers_carried = []
        bus_arrival = []
        bus_depart = []

        for node in range(0, len(current_bus)):

            # Take current node bus
            current_node = current_bus[node]
            capacity_check = 0

            # Append the information from this node to the relevant lists
            # First append the current stop
            stop_order.append(current_node.getStops())

            # Next the passengers
            passenger_manifest.append(current_node.getPassengers())

            # Then arrival and departures
            bus_arrival.append(current_node.getArrival())
            bus_depart.append(current_node.getArrival() + current_node.getWait())

            # Passenger capacity check
            for passengers in current_node.getPassengers():
                capacity_check = + passengers.capacity_cost
                passengers_carried.append(passengers)

            if capacity_check > list_of_buses[bus].bus_capacity:
                return False

        # print(stop_order)
        # print(passengers_carried)
        # print(passenger_manifest)

        # stop_order = [passenger_route[0][0], passenger_route[0][1], passenger_route[1][0],passenger_route[1][1],
        # passenger_route[2][0], passenger_route[2][1], passenger_route[3][0],passenger_route[3][1]]

        # For every passenger the bus carries validate that there is a route that picks them up and drops them off
        for passengers in passengers_carried:

            # Get the pick up and drop off stops for passenger
            pick = passenger_route[passengers.id][0]
            drop = passenger_route[passengers.id][1]

            # Set picked and dropped flags to false
            picked = False
            dropped = False

            # Check through the stop list and find the pick up stop
            for i in range(0, len(stop_order)):
                if stop_order[i] == pick:
                    picked = True

                    # Check the remain stops for the drop stop
                    for j in range(i, len(stop_order)):
                        if stop_order[j] == drop:
                            dropped = True
                            picked_stop = i
                            dropped_stop = j

            # Break if not picked or dropped
            if not picked or not dropped:
                return False

            # print(picked_stop)
            # print(dropped_stop)

            # Check the stops between the pick up and drop off stops to ensure that the passenger is on board
            for i in range(0, picked_stop):
                if passenger_manifest[i] == passengers:
                    return False

            for i in range(dropped_stop + 1, len(passenger_manifest)):
                if passenger_manifest[i] == passengers:
                    return False

            # Check all other stops to ensure the passenger isn't on board
            for i in range(picked_stop + 1, dropped_stop + 1):
                if passenger_manifest[i] != passengers:
                    return False

            if bus_depart[picked_stop] <= passenger_stop_arrival[passengers.id]:
                return False

            if bus_arrival[bus] >= passengers.dropoff_time:
                return False

    return True


# Generate a route that satisfies the passenger pick up and drop off requirements
def route_generator(passengers, buses, stops, depo):
    # Initialize the necessary lists
    generated_route = []
    non_visited_stops = []
    visited_stops = []
    passengers_picked = set()
    passengers_dropped = set()
    passengers_not_picked = passengers
    current_stop = []
    ind_bus = []
    wait = []
    setoff_time = []
    carried_passengers = []
    until = False

    # For each of the buses append a second dimension to the arrays
    for bus in range(0, len(buses)):
        current_stop.append([])
        ind_bus.append([])
        carried_passengers.append([])
        wait.append([])
        setoff_time.append([])
        non_visited_stops.append(set())
        visited_stops.append(set())

    # Append a third dimention
    for bus in range(0, len(buses)):
        current_stop[bus].append(depo)
        ind_bus[bus] = [Route.Route(depo, 0, 0, [])]
        carried_passengers[bus] = set()
        wait[bus] = 0
        setoff_time[bus] = 0
        non_visited_stops[bus] = set(stops)
        # non_visited_stops[bus] = stops
        visited_stops[bus] = set()
        # first_destination[bus] = start_stop.getNearStop(non_visited_stops)
        # visited_stops.add(near_stop)
        # non_visited_stops.remove(near_stop)

    # Loop until the conditions are satisfied
    while not until:
        for bus in range(0, len(buses)):
            extra_drop = False
            # If there exist any non-visited stops
            if bool(non_visited_stops[bus]):
                # print(non_visited_stops)

                # Get the nearest stop
                # near_stop = current_stop[bus][0].getNearStop(non_visited_stops[bus].copy())
                near_stop = get_nearest_stop(current_stop[bus][0], non_visited_stops[bus].copy())
                # near_stop = current_stop[bus][0].getRandStop(non_visited_stops[bus].copy())

                # print(near_stop.getStopId())

                # Add the stop to the visited stop list and remove it from the non_visited stop list
                visited_stops[bus].add(near_stop)
                for bus2 in range(0, len(buses)):
                    if near_stop in non_visited_stops[bus2]:
                        non_visited_stops[bus2].remove(near_stop)

            temp_list = []

            # Generate the list of carried passengers
            for passenger in carried_passengers[bus]:
                if passenger.getNearestDrop(stops.copy()) == near_stop:
                    temp_list.append(passenger)

            # If the stop is the destination of any passenger on the bus, drop them off
            for passenger in temp_list:
                carried_passengers[bus].remove(passenger)
                if passenger in passengers_picked:
                    passengers_picked.remove(passenger)
                    passengers_dropped.add(passenger)

            # If the stop is the nearest stop of any passenger pick them up
            for passenger in passengers:
                if passenger.getNearestStop(stops) == near_stop and passenger not in carried_passengers:
                    carried_passengers[bus].add(passenger)
                    passengers_picked.add(passenger)
                    passengers_not_picked.remove(passenger)
                    stops.append(passenger.getNearestDrop(list_of_stops))
                    non_visited_stops[bus].add(passenger.getNearestDrop(list_of_stops))

            if not bool(non_visited_stops[bus]) and bool(passengers_picked):
                for on_board_passenger in passengers_picked:
                    if on_board_passenger in carried_passengers[bus]:
                        near_stop = on_board_passenger.getNearestDrop(stops)
                        extra_drop = True

            if extra_drop:
                passengers_dropped.add(on_board_passenger)
                passengers_picked.remove(on_board_passenger)

            # Calculate arrival time
            # Worikng on changing to time stamp not calc
            # arrival_time = get_arrival(current_stop[bus][0], near_stop, setoff_time[bus], wait[bus])
            arrival_time = 1
            # TODO This needs some more real data, unilink?
            wait[bus] = wait_time()

            # Append the part of the route to the buses route
            ind_bus[bus].append(Route.Route(near_stop, arrival_time, wait[bus], carried_passengers[bus]))

            # Set current stop to the near_stop
            current_stop[bus][0] = near_stop

            # Set set off time to previous arrival time
            setoff_time[bus] = arrival_time

            # Check all passengers were picked up and dropped off
            if len(passengers_dropped) == len(list_of_passengers) and len(passengers_picked) == 0 and len(
                    passengers_not_picked) == 0:
                until = True

    # print(ind_bus)
    return ind_bus

# ----------------------------------------------------------------------------------------------------------------------

# Lookup the time between stops
def get_arrival(stop1, stop2, arrival, wait):
    return arrival + wait + stop_relations[int(stop1.id)][int(stop2.id)]


# Describe the routes of a bus in the console
def explore_bus_route(route, bus):
    # First Describe stop order and arrival time
    for stop in route:
        stop_id = stop.getStops().getStopId()
        stop_arrival = stop.getArrival()
        stop_wait = stop.getWait()

        print("Bus number: " + str(bus) + " arrives at stop: " + str(stop_id) + " at " +
              str(stop_arrival) + " and waits: " + str(stop_wait))


# Describe the routes of a passenger in the console
def explore_passenger_route(route):
    for passenger_id in range(0, len(route)):
        passenger_pick = route[passenger_id][0]
        passenger_drop = route[passenger_id][1]
        print("Passenger id: " + str(passenger_id) + " is picked up at stop " + str(passenger_pick.getStopId())
              + " and is dropped at stop " + str(passenger_drop.getStopId()))


# Get the order of stops the take buses within the route
def get_bus_order(route):
    order = []
    for stop in route:
        order.append(stop.getStops())

    return order

def ant_colony(list_of_stop_candidates, passenger_route, passengers):
    calc_probablity(list_of_stop_candidates)
    passengers_picked = set()
    passengers_dropped = set()
    passengers_not_picked = passengers
    non_visited_stops = []
    visited_stops = []
    ind_bus = []
    wait = []
    setoff_time = []
    carried_passengers = []

    for bus in range(0, len(list_of_buses)):
        carried_passengers.append([])
        ind_bus.append([])
        setoff_time.append([])
        wait.append([])
        non_visited_stops.append(set())
        visited_stops.append(set())

    for bus in range(0, len(list_of_buses)):
        setoff_time[bus] = 0
        wait[bus] = 0
        visited_stops[bus] = set()
        non_visited_stops[bus] = set(list_of_stop_candidates)
        carried_passengers[bus] = set()

    until = False

    while not until:
        extra_drop = False
        for bus in list_of_buses:

            if bool(non_visited_stops[bus.id]):
                best_stop = -1
                best_stop_ids = 0, 0
                current_stop_index = 0

                for stop in range(0, len(list_of_stops)):
                    if list_of_stops[stop] == bus.current_stop:
                        current_stop_index = stop

                for i in range(0, len(stop_probs[bus.id])):
                    for j in range(0, len(stop_probs[bus.id][i])):

                        if stop_probs[bus.id][i][j] >= best_stop and i == current_stop_index and i != j and \
                                list_of_stops[j] in non_visited_stops[bus.id]:
                            best_stop = stop_probs[bus.id][i][j]
                            best_stop_ids = i, j

                best_a, best_b = best_stop_ids

                best_stop_second = list_of_stops[best_b]

                # Remove from non visted stops add to visted stops
                if list_of_stops[best_b] in non_visited_stops[bus.id]:
                    non_visited_stops[bus.id].remove(list_of_stops[best_b])
                    visited_stops[bus.id].add(list_of_stops[best_b])

            temp_list = []

            # Generate the list of carried passengers
            for passenger in carried_passengers[bus.id]:
                if passenger_route[passenger.id][1] == best_stop_second:
                    temp_list.append(passenger)

            # If the stop is the destination of any passenger on the bus, drop them off
            for passenger in temp_list:
                carried_passengers[bus.id].remove(passenger)
                if passenger in passengers_picked:
                    passengers_picked.remove(passenger)
                    passengers_dropped.add(passenger)

            # If the stop is the nearest stop of any passenger pick them up
            for passenger in passengers:
                if passenger_route[passenger.id][0] == best_stop_second and passenger not in carried_passengers:
                    carried_passengers[bus.id].add(passenger)
                    passengers_picked.add(passenger)
                    passengers_not_picked.remove(passenger)

            if not bool(non_visited_stops[bus.id]) and bool(passengers_picked):
                for on_board_passenger in passengers_picked:
                    if on_board_passenger in carried_passengers[bus.id]:
                        for stop in range(0, len(list_of_stops)):
                            if list_of_stops[stop] == on_board_passenger.getNearestDrop(list_of_stop_candidates):
                                best_b = stop
                        extra_drop = True

            if extra_drop:
                passengers_dropped.add(on_board_passenger)
                passengers_picked.remove(on_board_passenger)

            # Calculate arrival time
            # TODO Change this to a look up of the stop time table
            arrival_time = calc_arrival(list_of_stops[best_a], list_of_stops[best_b], list_of_buses[bus.id].speed,
                                        setoff_time[bus.id], wait[bus.id])

            # TODO This needs some more real data, unilink?
            wait[bus.id] = wait_time()

            # Append the part of the route to the buses route
            ind_bus[bus.id].append(
                Route.Route(list_of_stops[best_b], arrival_time, wait[bus.id], carried_passengers[bus.id]))

            # Set current stop to the near_stop
            bus.current_stop = list_of_stops[best_b]
            print(best_b)

            # Set set off time to previous arrival time
            setoff_time[bus.id] = arrival_time

            pheromone_trails[best_a][best_b] += Q_const / float(stop_relations[best_a][best_b])

        if len(passengers_dropped) == len(list_of_passengers) and len(passengers_picked) == 0 and len(
                passengers_not_picked) == 0:
            until = True
    return ind_bus


def wait_time():
    return cntr_rnd.randint(0, 10000)

def evaluate_soloution(passenger_route, bus_route):
    current_passenger = None
    start = 0
    destination = 0
    total_passenger_travel = 0

    for i in range(0, len(passenger_route)):
        current_passenger = list_of_passengers[i]
        start, destination = passenger_route[i]
        total_passenger_travel += passenger_evaluate(current_passenger, start, destination)

    total_bus_travel = 0

    for j in range(0, len(bus_route)):
        total_bus_travel += bus_evaluate(bus_route[j])

    return total_bus_travel + total_passenger_travel


def passenger_evaluate(passenger, start, destination):
    passenger_start_x = passenger.xcord
    passenger_start_y = passenger.ycord
    passenger_dest_x = passenger.destination_x
    passenger_dest_y = passenger.destination_y

    time_to_start = passenger.calcTimeToTravel(passenger_start_x, start.lat, passenger_start_y, start.lang)
    time_to_dest = passenger.calcTimeToTravel(passenger_dest_x, destination.lat, passenger_dest_y, destination.long)

    return time_to_start + time_to_dest


def bus_evaluate(bus):
    return bus[-1].getArrival()


def calc_visablity(stop_i, stop_j):
    if stop_i != stop_j and float(stop_relations[stop_i.look_up_index][stop_j.look_up_index]) != 0:
        return 1 / float(stop_relations[stop_i.look_up_index][stop_j.look_up_index])
    else:
        return 0


def calc_probablity(stop_candidates):
    for bus in list_of_buses:
        sum_prob_of_stops = 0
        for stop_i in stop_candidates:
            for stop_j in stop_candidates:
                sum_prob_of_stops += (pheromone_trails[stop_i.look_up_index][stop_j.look_up_index] ** a_hyp) * \
                                     (calc_visablity(stop_i, stop_j) ** b_hyp)

        for stop_i in stop_candidates:
            for stop_j in stop_candidates:
                # print(    (((pheromone_trails[stop_i.look_up_index][stop_j.look_up_index] ** a_hyp) * (
                # calcVisablity(stop_i, stop_j) ** b_hyp)) / sum_prob_of_stops ) )
                stop_probs[bus.id][stop_i.look_up_index][stop_j.look_up_index] = \
                    (((pheromone_trails[stop_i.look_up_index][stop_j.look_up_index] ** a_hyp) * (
                            calc_visablity(stop_i, stop_j) ** b_hyp)) / sum_prob_of_stops)
                # print(stop_probs[bus.id][stop_i.look_up_index][stop_j.look_up_index] )
        # print(stop_probs)


def plot(list_of_stops, list_of_passengers, list_of_buses, passengers_route, bus_routes):
    # ----------------------  Plot figure

    for i in range(0, len(list_of_stops)):
        plt.plot(list_of_stops[i].lat, list_of_stops[i].long, 'bo', markersize=0.5)
        plt.annotate('%d' % i, (list_of_stops[i].lat + 2, list_of_stops[i].long))

    for i in range(0, len(list_of_passengers)):
        plt.plot(list_of_passengers[i].lat, list_of_passengers[i].long, 'r+')
        plt.plot(list_of_passengers[i].destination_x, list_of_passengers[i].destination_y, 'gx')
        plt.annotate('p_%d' % i, (list_of_passengers[i].lat + 2, list_of_passengers[i].long))
        plt.annotate('p_%d' % i, (list_of_passengers[i].destination_x + 2, list_of_passengers[i].destination_y))

    # for i in range(0, len(list_of_buses)):
    #    plt.plot(list_of_stops[list_of_buses[i].getStartStopId()].lat,
    #            list_of_stops[list_of_buses[i].getStartStopId()].long,
    #           'r>')

    for i in range(0, len(passengers_route)):
        plt.plot([list_of_passengers[i].lat, passengers_route[i][0].lat],
                 [list_of_passengers[i].long, passengers_route[i][0].long], ':g')

        plt.plot([list_of_passengers[i].destination_x, passengers_route[i][1].lat],
                 [list_of_passengers[i].destination_y, passengers_route[i][1].long], ':g')

    for i in range(0, len(bus_routes)):
        col = (np.random.random(), np.random.random(), np.random.random())
        for j in range(1, len(bus_routes[i])):
            plt.plot([bus_routes[i][j - 1].lat, bus_routes[i][j].lat],
                     [bus_routes[i][j - 1].long, bus_routes[i][j].long], c=col, linewidth=0.60)

    plt.show()


def get_nearest_stop(stop, stop_candidates):
    current_nearest = 100000000000
    near_stop = None
    to_list = list(stop_candidates)
    for destinations in to_list:
        if float(stop_relations[stop.look_up_index][destinations.look_up_index]) <= float(current_nearest) and \
                (destinations != stop):
            current_nearest = stop_relations[stop.look_up_index][destinations.look_up_index]
            near_stop = destinations

    return near_stop


###------------- Main run Start

# calcProbablity(1, list_of_stops)

routes = run("greedy")

explore_passenger_route(passenger_bookings)

bus_routes = []

for i in range(0, len(routes)):
    bus_routes.append(get_bus_order(routes[i]))
    print(explore_bus_route(routes[i], i))
# bus_routes = [getBusOrder(routes[0]), getBusOrder(routes[1]), getBusOrder(routes)]

plot(list_of_stops, list_of_passengers, list_of_buses, passenger_bookings, bus_routes)

# run(None)