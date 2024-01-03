class Schedule:
    """
    For static routes there needs to be a control class to manage their current and future routes. These routes contain
    a list of stop (due to some poor naming on my part this uses the Stop class), its daily frequency and the type of
    vehicle allowed to use it.

    :param route_list: This is the list of route objects that the vehicle takes in order. This should include timing
                       details for the route.
    :type route_list: List<Route>

    :param allowed_vehicles: Set the allowed vehicle type
    :type allowed_vehicles: str




    """
    def __int__(self, schedule_id, route_list, allowed_vehicles):
        self.route_list = route_list
        self.allowed_vehicles = allowed_vehicles
        self.schedule_id = schedule_id

    def add_route_to_schedule(self, route):
        self.route_list.append(route)

    def change_vehicle_type(self, type):
        self.allowed_vehicles = type



        

