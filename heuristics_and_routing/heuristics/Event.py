"""
Event class hold the information used for an event including, start action, end action, relevent agents, position, and
timing

Intended usage: If you are making changes here you are modifying the events and what they contain not how they are
handled

"""

class Event:

    def __init__(self, start_or_end, relevant_agents, position_x, position_y, tick_occurrence):
        """Constructor method"""
        self.start_or_end = start_or_end

        self.relevant_agents = relevant_agents

        self.position_x = position_x
        self.position_y = position_y
