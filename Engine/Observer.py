"""
Class for observer. Each observer has a set list of event triggers that it can see


Intended usage: Changing things here changes how the observers function

:param watching_events: What events this specific observer is watching
:type watching_events: list<Events>
"""


class Observer:

    def __init__(self, watching_events):
        # Set the list for events that the observer watches for
        self.watching_events = watching_events

    def give_watched_events(self):
        """
        Return the watched events

        :return: Watched events
        :rtype: list<Events>

        """

        return self.watching_events

    def is_event_watched(self, event):
        """
        Checks if provided event is watched by specific observer

        :return: If event is watched by observer
        :rtype: bool
        """

        return bool(event in self.watching_events)
