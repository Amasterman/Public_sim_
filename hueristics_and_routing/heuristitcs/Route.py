class Route:
    def __init__(self, stop, arrival_time, wait_time, passenger_manifest):
        self.stop = stop
        self.arrival_time = arrival_time
        self.wait_time = wait_time
        self.passenger_manifest = passenger_manifest

    def getPassengers(self):
        return self.passenger_manifest

    def getStops(self):
        return self.stop

    def getArrival(self):
        return self.arrival_time

    def getWait(self):
        return self.wait_time