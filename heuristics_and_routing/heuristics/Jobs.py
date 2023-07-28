class Jobs:
    """ Jobs act as a dataset containing information on weight, arrival time and type
        Intended usage: If you are making changes here you are modifying the data that a job (A section of a route) has

     :param weight: Current carry weight
     :type weight: int

     :param arrival_date: Date of arrival
     :type arrival_date: date

     :param type: Type of job
     :type type: str

     """

    def __init__(self, weight, arrival_date, type):
        """Constructor method"""
        self.weight = weight
        self.arrival_date = arrival_date
        self.type = type