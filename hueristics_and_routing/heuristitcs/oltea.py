# Initial setup
import math
import time
import argparse

import csv

import matplotlib.pyplot as plt
import numpy as np
from math import radians, sin, cos, sqrt, atan2,acos, pi

import Buses as Bus
import Passenger as Pass
import Route as Route
import Stops as Stop


import logging
import pdb

import openpyxl

import datetime



# Create a new Excel workbook and select the worksheet
workbook = openpyxl.load_workbook("result.xlsx")
worksheet = workbook.active

# Configure logging
logging.basicConfig(filename='oltea.log', level=logging.INFO)

# Area of longitude and latitude of the greater Southampton area [Better way to define?]
minlat = 50.8255000
minlon = -1.6263000
maxlat = 51.0142000
maxlon = -1.0873000

now = datetime.datetime.now()
print(now)


parser=argparse.ArgumentParser()
parser.add_argument('--seed', type=int, default=None, help='random seed')
parser.add_argument('--buses', type=int, default=None, help='number of buses')
parser.add_argument('--passengers', type=int, default=None, help='number of passengers')
parser.add_argument('--index', type=int, default=None, help='run index')
parser.add_argument('--stops', type=int, default=None, help='number of stops')
args=parser.parse_args()

seed=args.seed
no_buses=args.buses
no_passengers=args.passengers  
index=args.index
break_count = args.stops

rnd=np.random
rnd.seed(seed)

max_lateness=15
max_bus_cap=15
MAX_CLUSTER_DISTANCE=1000

dynamic=False

# Passenger bookings in advance within a dynamic system
passenger_bookings = []

# List of stop locations
list_of_stops = []

# Stop importer; IN XML scraped from www.openstreetmap.org OUT List of stop objects
# Open file with CSV reader
with open("XML_to_CSV_OUT.CSV", newline='') as csvfile:
    # Skip header line
    next(csvfile)

    # Break count will limit the amount of stops imported. << means all included
    
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
depo = list_of_stops[rnd.randint(0, no_stops)]

# Random bus generator
# TODO Need to get some more info on the buses in the area, unilink and bluestar maybe?
for i in range(0, no_buses):
    # Generate vehicle with random parameters, also potential to be renamed
    temp_bus = Bus.Buses(i, depo, rnd.randint(4, max_bus_cap), rnd.randint(30, 70),
                         rnd.randint(1, 4), depo)

    # Append to list
    list_of_buses.append(temp_bus)

# -----------------------  Passenger settings

# List of passengers
list_of_passengers = []

# TODO All of this is subject to change, this data is kinda unknowable until the surveys are complete



# Two versions for static and dynamic versions. Decided by the preivously declared global variable.
if dynamic:
    # Generate up to the target number of passengers
    for i in range(0, no_passengers):
        # Generate random passenger data including if the trip has been booked in advance
        temp_passenger = Pass.Passenger(i, rnd.uniform(minlat, maxlat), rnd.uniform(minlon, maxlon),
                                        rnd.uniform(minlat, maxlat),
                                        rnd.uniform(minlon, maxlon), rnd.randint(1, 4), rnd.randint(1, 100),
                                        rnd.randint(1, 3), now, now,
                                        bool(random.getrandbits(1)), max_lateness)

        # Append to list of passengers
        list_of_passengers.append(temp_passenger)
else:
    # Generate random passenger data the prebooked flag is set to 1
    for i in range(0, no_passengers):
        temp_passenger = Pass.Passenger(i, rnd.uniform(minlat, maxlat), rnd.uniform(minlon, maxlon),
                                        rnd.uniform(minlat, maxlat),
                                        rnd.uniform(minlon, maxlon), rnd.randint(1, 4), rnd.randint(1, 100),
                                        rnd.randint(1, 3), now,now, 1,
                                        max_lateness)

        # Append to list of passengers
        list_of_passengers.append(temp_passenger)

# ----------------------- Dynamic setup

# Two lists; passengers booked more than a day in advance/repeat trips, and new requests
passenger_booked = []
passenger_not_booked = []

# run the system on the provided method and time the time it takes to run
def run():
    # Take the computer time before the run
    start_time = time.perf_counter()

    # Dived the selection by dynamic and static
    if dynamic:
        # Init Dynamic
        int_dynamic()

        # Switch statement for selecting the heuristic
        # Ok no switch statment thats in python 3.10 and im not updatitng and breaking everything again
 
        return greedy_online()

    else:

        # Init Static
        list_of_active_stops, passenger_bookings = ini_static()
        return greedy_offline(list_of_active_stops, passenger_bookings)

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
    # clusters=create_clusters(list_of_passengers)
    # list_of_active_stops, passenger_bookings = calculate_pickup_locations(clusters, list_of_stops)

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
    logging.info("===== NEW RUN %d =====", index)
    logging.info("Seed: %d", seed)
    logging.info("Buses: %d", no_buses )
    logging.info("Passengers: %d", no_passengers)
        
    return route_generator(list_of_passengers.copy(), list_of_buses.copy(), list_of_active_stops, depo)


# Define a function to create clusters based on passenger locations
def create_clusters(passengers):
    clusters = []
    for passenger in passengers:
        added_to_cluster = False
        lat=passenger.getNearestStop(list_of_stops).lat
        long=passenger.getNearestStop(list_of_stops).long
        for cluster in clusters:
            if calc_distance(lat,long, cluster['lat'],cluster['long']) <= MAX_CLUSTER_DISTANCE:
                cluster['members'].append(passenger)
                added_to_cluster = True
                break
        if not added_to_cluster:
            clusters.append({'lat': lat,'long':long, 'members': [passenger]})
    return clusters


# Define a function to calculate the central pickup location for each cluster
def calculate_pickup_locations(clusters, route):
    for x in range(0, len(list_of_passengers)):
        passenger_bookings.append([])
    pickup_locations = []
    for cluster in clusters:
        nearest_stop = None
        min_distance = math.inf
        for stop in route:
            d = calc_distance(cluster['lat'],cluster['long'],stop.lat,stop.long)
            if d < min_distance:
                nearest_stop = stop
                min_distance = d
        for passenger in cluster['members']:
            passenger_bookings[passenger.id]=[nearest_stop, passenger.getNearestDrop(list_of_stops)]
        pickup_locations.append( nearest_stop)
    return pickup_locations, passenger_bookings

# Return all stops in use for this set of passengers and the booking register
def user_stops():
    # Get the Greedy nearest pick and drop stops
    # TODO improve this away from a greedy method
    for p in passenger_booked:
            nearest_stop=p.getNearestStop(list_of_stops)
            nearest_drop=p.getNearestDrop(list_of_stops)
            
            passenger_bookings.append([nearest_stop, nearest_drop])
            
            time_to_stop = calc_walk_time(nearest_stop.lat, nearest_stop.long, p.lat, p.long)
            pickup_time = now+ datetime.timedelta(minutes=time_to_stop)
            p.set_pickup_time(pickup_time)
            
            time_to_drop = calc_arrival(nearest_stop, nearest_drop, 0)
            time_to_drop+=time_to_drop*0.25+max_lateness
            drop_time = now+ datetime.timedelta(minutes=time_to_drop)
            p.set_dropoff_time(drop_time)
            
    # Initialize an empty set
    list_of_active_stops = set()

    i=0
    # Take start stop elements from passenger bookings and add to the list of active stops
    for elements in passenger_bookings:
        one, two = elements
        if one not in list_of_active_stops :
            list_of_active_stops.add(one)
        i=i+1

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

# The utility function is calculated for each passenger and each pair of buses that the passenger can transfer between.
# make the funciton to calculate the utility
def naive_utility(passenger, bus1, bus2,destination,stay_convenience, transfer_convenience):
    # make the weights
    w1 = 1
    w2 = 1
    
    w3 = 1 + stay_convenience
    w4 = 1 + stay_convenience
    
    w5 = 1 + transfer_convenience
    w6 = 1 + transfer_convenience

    # make the variables
    d_b1_b2 = calc_distance(bus1.lat, bus1.long, bus2.lat, bus2.long)
    t_b1_b2 = calc_arrival(bus1, bus2,0)
    
    d_b1_d = calc_distance(bus1.lat, bus1.long, destination.lat, destination.long)
    t_b1_d = calc_arrival(bus1, destination,0)
    
    d_b2_d = calc_distance(bus2.lat, bus2.long, destination.lat, destination.long)
    t_b2_d = calc_arrival(bus2, destination,0)
    
    if d_b1_b2 > d_b1_d or d_b1_b2 > d_b2_d:
        return 0
        
    if t_b1_b2 > t_b1_d or t_b1_b2 > t_b2_d:
        return 0
    
    # calculate the utility
    utility = w3*d_b1_d-w5*d_b2_d + w4*t_b1_d-w6*t_b2_d

    print("utility",utility)
    return utility/1000
    
loop=0

def check_infinite_loop(non_visited):
    global loop
    for bus in range (0, len(non_visited)):
        if len(non_visited[bus])>0:
            return False
    loop+=1
    return True 


# Generate a route that satisfies the passenger pick up and drop off requirements
def route_generator(passengers, buses, stops, depo):
    # Initialize the necessary lists
    non_visited_stops = []
    
    pickups = []
    dropoffs = []
    
    monitored_passengers = []
    passenger_transfers={}
    transfer_stop = []
    visited_stops = []
    passengers_picked = set()
    passengers_dropped = set()
    passengers_not_picked = passengers
    current_stop = []
    ind_bus = []
    next_stops = []
    wait = []
    setoff_time = []
    carried_passengers = []
    until = False
    
    transfer_relations = []
    dissatisfied_passengers = []
    
    total_wait = 0
    total_distance = 0
    total_time = 0

    # For each of the buses append a second dimension to the arrays
    for bus in range(0, len(buses)):
        current_stop.append([])
        ind_bus.append([])
        carried_passengers.append([])
        wait.append([])
        setoff_time.append([])
        non_visited_stops.append(set())
        pickups.append(set())
        dropoffs.append(set())
        visited_stops.append(set())
        next_stops.append([])
        transfer_relations.append([])

    # Append a third dimention
    for bus in range(0, len(buses)):
        current_stop[bus].append(depo)
        ind_bus[bus] = [Route.Route(depo, now, now,0, 0, [])] # ind_bus[0][5][1] the 1st bus, the6th stop, time
        carried_passengers[bus] = set()
        wait[bus] = 0
        setoff_time[bus] = 0
        non_visited_stops[bus] = set(stops)
        pickups[bus] = set(stops)
        dropoffs[bus] = set()
        visited_stops[bus] = set()
        next_stops[bus] = None
    

    # Loop until the conditions are satisfied
    while not until:
        for bus in range(0, len(buses)):
            print ("Bus: ", bus)
            extra_drop = False
            global loop
            check_infinite_loop(non_visited_stops)
            
            if loop>10:
                return  
            
            if bool(pickups[bus]) or bool(dropoffs[bus]):  
                available_stops = pickups[bus].union(dropoffs[bus])
            
                near_stop = get_nearest_stop(current_stop[bus][0], available_stops)
                    
                # Add the stop to the visited stop list and remove it from the non_visited stop list
                visited_stops[bus].add(near_stop)
                if near_stop in dropoffs[bus]:
                    dropoffs[bus].remove(near_stop)
                    
                for bus2 in range(0, len(buses)):
                    if near_stop in pickups[bus2]:
                        pickups[bus2].remove(near_stop)
                    if near_stop in non_visited_stops[bus2]:
                        non_visited_stops[bus2].remove(near_stop)
            
                
                temp_carried_passengers = [] #if theres multiple passengers at the same stop, check all

                # Calculate arrival time

                # The delay time of the bus to arrive at the stop 
                wait[bus] = 0

                # The time it took to get to the stop
                arrival_time = calc_arrival(current_stop[bus][0], near_stop, wait[bus])

                arrival=ind_bus[bus][-1].getSetOff()+datetime.timedelta(minutes=arrival_time)
                current_time=arrival

                # The distance between the current stop and the next stop
                distance=calc_distance(current_stop[bus][0].lat, current_stop[bus][0].long, near_stop.lat, near_stop.long)

                # Add the time to all passengers carried by this bus
                for passenger in carried_passengers[bus]:
                    passenger.increase_total_time(arrival_time)
                    passenger.set_current_pos(near_stop.lat,near_stop.long)

                # Generate the list of carried passengers
                for passenger in carried_passengers[bus]:
                    if passenger.getNearestDrop(stops.copy()) == near_stop:
                        temp_carried_passengers.append(passenger)

                # If the stop is the destination of any passenger on the bus, drop them off
                for passenger in temp_carried_passengers:
                    carried_passengers[bus].remove(passenger)

                    if passenger in passengers_picked:
                        passengers_picked.remove(passenger)
                        passengers_dropped.add(passenger)

                        distance_to_dest = calc_distance(near_stop.lat,near_stop.long, passenger.destination_x, passenger.destination_y)
                        # time_to_dest = calc_walk_time(near_stop.lat,near_stop.long, passenger.destination_x, passenger.destination_y)

                        # passenger.increase_total_time(time_to_dest)
                        passenger.increase_total_distance(distance_to_dest)
                        passenger.set_current_pos(near_stop.lat,near_stop.long)
                        # check if the passenger is dissatisfied
                        if passenger.get_dropoff_time() >current_time :
                            passenger.set_dissatisfaction(True)
                            print("Dissatisfied passenger", passenger.id,)
                            dissatisfied_passengers.append(passenger)

                        print ("\n<<<<<<<<<<<<<<<<<<< Dropped off passenger", passenger.id, "at stop", str(near_stop.getStopId())[:5],"by bus", bus,"\n")

                if len(transfer_relations[bus]) > 0:
                    for passenger in transfer_relations[bus]:
                        pickups[bus].add(passenger.getNearestStop(list_of_stops))
                        non_visited_stops[bus].add(passenger.getNearestStop(list_of_stops))
                        
                temp_carried_passengers = []
                for passenger in passengers_not_picked:
                    if passenger.getNearestStop(stops.copy()) == near_stop:
                        temp_carried_passengers.append(passenger)

                # If the stop is the nearest stop of any passenger pick them up
                for passenger in temp_carried_passengers    :

                            carried_passengers[bus].add(passenger)
                            passengers_picked.add(passenger)
                            passengers_not_picked.remove(passenger)

                            stops.append(passenger.getNearestDrop(list_of_stops))
                            non_visited_stops[bus].add(passenger.getNearestDrop(list_of_stops))
                            dropoffs[bus].add(passenger.getNearestDrop(list_of_stops))

                            distance_to_stop = calc_distance(near_stop.lat,near_stop.long, passenger.lat, passenger.long)
                            time_to_stop = calc_walk_time(near_stop.lat,near_stop.long, passenger.lat, passenger.long)
                            passenger.increase_total_time(time_to_stop)
                            passenger.increase_total_distance(distance_to_stop)
                            passenger.set_current_pos(near_stop.lat,near_stop.long)
                            print ("\n>>>>>>>>>>>>>>>>> Picked up passenger", passenger.id, "at stop", str(near_stop.getStopId())[:5],"by bus", bus,"\n")

                for passenger in passengers_picked.copy():
                    if passenger in carried_passengers[bus].copy() and passenger.getStartStop(list_of_stops) != near_stop and passenger not in monitored_passengers:
                        for bus2 in range(len(buses)):
                            transfer_rate=0
                            if bus2!=bus and passenger.prev_bus!=bus2 :
                                destination=passenger.getNearestDrop(list_of_stops)
                                temp_carried=carried_passengers[bus2].copy()
                                temp_carried.add(passenger)

                                stay_convenience=get_convenience(carried_passengers[bus],destination)
                                transfer_convenience=get_convenience(temp_carried,destination)
                        
                                transfer_rate=naive_utility(passenger,near_stop,ind_bus[bus2][-1].getStops(),destination, stay_convenience, transfer_convenience)
                                print("Utility: ",transfer_rate)
                                
                            if transfer_rate>0 :
                     
                                passengers_not_picked.append(passenger)
                                passengers_picked.remove(passenger)
                                carried_passengers[bus].remove(passenger)
                                if passenger.getNearestDrop(list_of_stops) in non_visited_stops[bus]:
                                    non_visited_stops[bus].remove(passenger.getNearestDrop(list_of_stops))
                                if passenger.getNearestDrop(list_of_stops) in dropoffs[bus]:
                                    dropoffs[bus].remove(passenger.getNearestDrop(list_of_stops))

                                non_visited_stops[bus2].add(near_stop)
                                pickups[bus2].add(near_stop)
                                
                                monitored_passengers.append(passenger)
                                passenger.set_current_pos(near_stop.lat,near_stop.long)
                                passenger.prev_bus=bus
                                
                                print("Transfer passenger: ",passenger.id,"from",bus," to bus ",bus2)
                                break
                            
                print("Transfer passengers: ",str(len(monitored_passengers)))

                listss=list(passengers_not_picked)
                print("Not picked",str(len(listss)))
                print("Picked",str(len(passengers_picked)))
                print("Dropped",str(len(passengers_dropped)))
                print("Disss",str(len(dissatisfied_passengers)))
                # Set current stop to the near_stop

                # for passenger in passengers_picked:
                #     print(passenger in carried_passengers[bus])
                #     print(passenger.getNearestDrop(list_of_stops).getStopId()==near_stop.getStopId())

                ind_bus[bus].append(Route.Route(near_stop,current_time, arrival,distance, wait[bus], carried_passengers[bus]))
                current_stop[bus][0] = near_stop
                # print("Current stop: ",current_stop[bus][0].getStopId())

                for stop in non_visited_stops[bus]:
                    print(stop.getStopId())

                    # Check all passengers were picked up and dropped off
            if len(passengers_dropped) == len(list_of_passengers) and len(passengers_picked) == 0 and len(
                    passengers_not_picked) == 0:
                until = True

    wait[bus] = 0
    arrival=ind_bus[bus][-1].getSetOff()+datetime.timedelta(minutes=arrival_time)
    set_off=arrival+datetime.timedelta(minutes=wait[bus])
    distance=calc_distance(current_stop[bus][0].lat, current_stop[bus][0].long, depo.lat, depo.long)
    for bus in range(0, len(buses)):
        ind_bus[bus].append(Route.Route(depo,set_off, arrival_time,distance, wait[bus], carried_passengers[bus]))
    
    save_results(ind_bus)
    
    return ind_bus

def save_results(ind_bus):
    
    total_wait = 0
    total_distance = 0
    total_time = 0
    for bus in range(0, len(list_of_buses)):
        for route in ind_bus[bus]:
            total_wait += route.getWait()
            total_distance += route.getDistance()
    
    for bus in range(0, len(list_of_buses)):
        start = ind_bus[bus][0].getArrival()
        end= ind_bus[bus][-1].getSetOff()
        total_time += (end-start).total_seconds()/60

    logging.info("Total wait time: %d minutes", total_wait)
    logging.info("Avegera distance per bus: %d km", total_distance/len(list_of_buses))
    logging.info("Average bus time: %d hours", total_time/len(list_of_buses))
    
    print("Total wait time: ", total_wait)
    print("Avegera distance per bus: ", total_distance/len(list_of_buses))
    print("Average bus time: ", total_time/len(list_of_buses))
    
    average_passenger_time = 0
    for passenger in list_of_passengers:
        average_passenger_time += passenger.get_total_time()
        
    average_passenger_time = average_passenger_time/len(list_of_passengers)
    
    logging.info("Average passenger time: %d hours", average_passenger_time)
    print("Average passenger time: ", average_passenger_time%1000)
    
    data = [["new_heuristic",no_buses,no_passengers,total_distance%1000, total_time%60, total_wait]]
    
    for row in data:
        worksheet.append(row)
        
    workbook.save("result.xlsx")

def get_convenience(passengers, stop):
    stay_convenience = 0
    for passenger in passengers:
        if passenger.getNearestDrop(list_of_stops) == stop:
            stay_convenience += 1
    return stay_convenience

# Calcute the time it takes the bus to travel from stop1 to stop2
def calc_arrival(stop1, stop2, wait):
    # Average speed of a bus in m/min inside city
    speed=417
  
    return wait + (calc_distance(stop1.lat, stop1.long, stop2.lat, stop2.long) / speed)

def calc_walk_time(x,y,a,b):
    # Average walking speed in m/min
    speed=90
    return calc_distance(a, b, x, y) / speed

def calc_distance(lat1, lon1, lat2, lon2):
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

def unique_dropoff(list_of_passengers, stop):
    for passenger in list_of_passengers:
        if passenger.getNearestDrop(list_of_stops) == stop:
            return False
    return True

# Get the order of stops the take buses within the route
def get_bus_order(route):
    order = []
    for stop in route:
        order.append(stop.getStops())
    return order

# Return random wait time between 0 and 20 minutes
def wait_time():
    return rnd.randint(0, 20)

def plot(list_of_stops, list_of_passengers, list_of_buses, passenger_bookings, bus_routes):
    # ----------------------  Plot figure

    # Plot the stops
    for i in range(0, len(list_of_stops)):
        plt.plot(list_of_stops[i].lat, list_of_stops[i].long, 'bo', markersize=0.5)
        plt.annotate('%d' % i, (list_of_stops[i].lat + 2, list_of_stops[i].long))

    # Plot the passengers origins and destinations
    for i in range(0, len(list_of_passengers)):

        plt.text(list_of_passengers[i].origin_x, list_of_passengers[i].origin_y, list_of_passengers[i].id, ha="center", va="center")
        plt.text(list_of_passengers[i].destination_x,list_of_passengers[i].destination_y, "^"+str(list_of_passengers[i].id)+"^")
        plt.plot(list_of_passengers[i].destination_x, list_of_passengers[i].destination_y, 'gx')
        plt.annotate('p_%d' % i, (list_of_passengers[i].origin_x + 2, list_of_passengers[i].origin_y))
        plt.annotate('p_%d' % i, (list_of_passengers[i].destination_x + 2, list_of_passengers[i].destination_y))
    
    # Plot the passengers walk routes
    for i in range(0, len(passenger_bookings)):
            plt.plot([list_of_passengers[i].origin_x, passenger_bookings[i][0].lat],
                     [list_of_passengers[i].origin_y, passenger_bookings[i][0].long], ':r')

            plt.plot([list_of_passengers[i].destination_x, passenger_bookings[i][1].lat],
                     [list_of_passengers[i].destination_y, passenger_bookings[i][1].long], ':m')

    # Plot the buses routes
    for i in range(0, len(bus_routes)):
        col = (np.random.random(), np.random.random(), np.random.random())
        for j in range(1, len(bus_routes[i])):
            plt.plot([bus_routes[i][j - 1].lat, bus_routes[i][j].lat],
                     [bus_routes[i][j - 1].long, bus_routes[i][j].long], c=col, linewidth=0.90, marker='D')
   
    plt.title('Transfer system')
    plt.show()

def get_nearest_stop(stop, stop_candidates):
    
    if len(stop_candidates) == 1:
        return list(stop_candidates)[0]
    
    current_nearest = 100000000000
    near_stop = None
    to_list = list(stop_candidates)
    for destinations in to_list:
        if float(stop_relations[stop.look_up_index][destinations.look_up_index]) <= float(current_nearest) and \
                (destinations != stop):
            current_nearest = stop_relations[stop.look_up_index][destinations.look_up_index]
            near_stop = destinations

    return near_stop

def get_nearest_stop_and_exclude(stop, stop_candidates,exclude):
    
    current_nearest = 100000000000
    near_stop = None
    to_list = list(stop_candidates)
    for destinations in to_list:
        if float(stop_relations[stop.look_up_index][destinations.look_up_index]) <= float(current_nearest) and \
                (destinations != stop) and (destinations != exclude):
            current_nearest = stop_relations[stop.look_up_index][destinations.look_up_index]
            near_stop = destinations

    return near_stop

def get_middle_stop(start_stop, end_stop, stop_candidates):
    start_index = start_stop.look_up_index
    end_index = end_stop.look_up_index
    current_optimal_distance = 100000000000
    optimal_stop = None
    
    for stop in stop_candidates:
        stop_index = stop.look_up_index
        distance_to_start = float(stop_relations[start_index][stop_index])
        distance_to_end = float(stop_relations[stop_index][end_index])
        total_distance = distance_to_start + distance_to_end
        
        if total_distance < current_optimal_distance:
            current_optimal_distance = total_distance
            optimal_stop = stop
    
    return optimal_stop


###------------- Main run Start

routes = run()

bus_routes = []

for i in range(0, len(routes)):
    bus_routes.append(get_bus_order(routes[i]))
    # print(explore_bus_route(routes[i], i))
    

# bus_routes = [getBusOrder(routes[0]), getBusOrder(routes[1]), getBusOrder(routes)]

# plot(list_of_stops, list_of_passengers, list_of_buses, passenger_bookings, bus_routes)

