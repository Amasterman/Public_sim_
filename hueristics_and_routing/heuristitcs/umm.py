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
            #Worikng on changing to time stamp not calc
            #arrival_time = get_arrival(current_stop[bus][0], near_stop, setoff_time[bus], wait[bus])
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