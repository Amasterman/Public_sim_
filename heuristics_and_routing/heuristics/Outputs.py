"""
This is the class that handles the outputs of the system. This includes the logs (i.e a dense record of the runs) and
the generation of graphs and images.

Intended usage: If you are making changes here you are changing the outputs that are calculated from the output data of
the world enviornemnt.

"""


class Outputs:
    """
    :param data_packet: When handling an output the log name/location is sent as a str pointing towards the file name/
                        location
    :type data_packet: str



    """
    def __init__(self, data_packet):

        self.data_packet = data_packet
        