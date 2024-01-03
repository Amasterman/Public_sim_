"""
Event class hold the information used for an event including, start action, end action, relevent agents, position, and
timing

Intended usage: If you are making changes here you are modifying the events and what they contain not how they are
handled

:param start_or_end: If the event is the start or the end of an action
:type start_or_end: bool

:param relevant_agents: What agents are affected by the event
:type relevant_agents: Agent TODO Same problem here need to better define agent

:param position_x: Position of the event in the X axis
:type position_x: float

:param position_y: Position of the event in the Y axis
:type position_y: float

:param tick_occurrence: What tick the event has occurred on
:type tick_occurrence: int

:param action: What tye of action the event is
:type action: str
"""


class Event:

    def __init__(self, start_or_end, relevant_agents, position_x, position_y, tick_occurrence, action):
        """Constructor method"""
        self.start_or_end = start_or_end

        self.relevant_agents = relevant_agents

        self.position_x = position_x
        self.position_y = position_y

        self.tick_occurrence = tick_occurrence

        self.action = action

    def get_start_or_end(self):
        """
        Getter for getting weather the event is the start or end of an event

        :return: start or end of event
        :rtype: bool

        """

        return self.start_or_end

    def get_relevant_agents(self):
        """
        Getter for the agents that are affected by the event

        :return: agents affected by the event
        :rtype: list<agents>

        """
        return self.relevant_agents

    def get_pos(self):
        """
        Getter for position coords for the event

        :return: a tuple of the x and y coords
        :rtype: float, float

        """
        return self.position_x, self.position_y

    def get_action(self):
        """
        Getter for what the event actually is

        :return: return event type
        :rtype: str

        """
        return self.action

    def tick_occurrence(self):
        """
        Getter for what tick the event occurred on

        :return: tick event occurred on
        :rtype: int

        """
        return self.tick_occurrence
