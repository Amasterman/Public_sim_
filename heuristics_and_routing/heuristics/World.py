"""
This class acts as the main body of the simulator.

The world sim will progress thorough ticks set by the tick rate and when an agent action is required an event will be
thrown.

The world state will be queryable returning all the stops with active elements, here meaning either has a passenger or
bus waiting, current bus positions, either a single stop or travelling a link between them (optionally with the time
steps remaining), and passenger agent information. The passenger agent information will have various levels of
queeryable data, but the full breadth of possible information is current location, current stop, target stop, capacity,
current bus

Events are classified as agents beginning an action and finishing an action.

Events will be thrown to different observers depending on the level of data allowed to the subscribers. This is a bit
arbitrary but important. By having varying levels of knowlage divided by subscribers you are able to adjust how much
the routeing algs have access to. The full events list being thrown is needed for logging.

:param passenger_agents: List of active passenger agents
:type passenger_agents: list<Passenger>

:param bus_agents: List of active bus agents
:type bus_agents: list<Bus>

:param time_step: How often the world returns events
:type time_step: int

"""


class World:

    def __init__(self, passenger_agents, bus_agents, time_step):
        """Constructor class"""

        # Init ticks

        self.tick_step = 0

        # Init rate that observers send event data
        self.time_step = time_step

        # Init agent sets
        self.passenger_agents = passenger_agents
        self.bus_agents = bus_agents

        # Init observers probably going to have more of these
        self.full_observer = []
        self.routing_observer = []

        # Init Event subs
        self.event_subs = []

        # Take actionsets from the agents into a list indexed the same way as the agent_list
        for passenger in self.passenger_agents:
            self.passenger_agents_action_sets = passenger.get_action_set

    def tick_up(self):
        """
        Increment the ticks of the world
        """
        # tock
        self.tick_step += 1

    def tick(self, triggers, subscribers):
        """
        Execute the standard procedure of the world

        send triggers to subs

        serve subs


        inc tick
        """
        if self.tick_step % self.time_step:

            for event in triggers:
                for subscriber in subscribers:
                    if subscriber.is_event_watched(event):
                        self.trigger_subs(subscriber, event)

            for subscriber in subscribers:
                self.serve_sub(subscriber)

        self.tick_up()

    def trigger_subs(self, subscribers, event):

        """
        Serve subscribed observers events
        """

        for observer in subscribers:
            observer.append(event)
            observer.set_notify(True)

    def serve_sub(self, subscriber):

        """
        Return each observer that has had an event trigger this timestep
        """
        out_sub = []

        for observer in subscriber:
            if observer.notify:
                observer.set_notify(False)
                out_sub.append(observer.out)

        return out_sub

    def make_event(self, start_or_end, agent, action):
        """
        Pass in relevant info into a event class object and return it

        In this case the relevant info needed only relate the action (what tye of action and if its a start or end) and
        what agent is affected

        :param start_or_end: start_or_end of event
        :type start_or_end: bool

        :param agent: affected agent
        :type agent: Agent TODO Uhh thinking on this may need to set up some inheritance/interface for agents to use

        :param action: What action is occurring
        :type action: str

        :return: Event class built from parameters
        :rtype: Event
        """
        pass
