"""
Meta class for agents (For those unfamiliar with python these are the equivalent of interfaces, they cant be 
instantiated and must be inherited by other classes). In this case the


"""
from abc import ABCMeta, abstractmethod


class Agent(metaclass=ABCMeta):

    def __init__(self, pos_x, pos_y):
        """Constructor Class"""
        self.current_action = None

        # X y positions
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.list_of_actions = None

    def get_current_action(self):
        """
        Method to call and get the current action of the agent

        :return: Return the current action of the agent
        :rtype: str
        """
        return self.current_action

    @abstractmethod
    def decide_next_action(self):
        """
        This is a method that must be overwritten by the inheriting class
        """

    def move_agent(self, delta_x, delta_y):
        """
        Change the x y coords of the agent by the provided x y amounts

        :param delta_x: The amount to change the x coord of the agent by
        :type delta_x: float

        :param delta_y: The amount to change the y coord of the agent by
        :type delta_y: float

        """

        self.pos_x += delta_x
        self.pos_y += delta_y

    def get_possible_actions(self):
        """
        Return the set of possible actions that the agent can preform

        :return: return the list of possible actions by the agents
        :rtype: list<str>
        """

        return self.list_of_actions

    def add_possible_actions(self, actions):
        """
        Take a set of actions and add them to the list of actions

        """

        for action in actions:
            self.list_of_actions.append(action)

    def remove_possible_actions(self, actions):

        for action in actions:
            if action in self.list_of_actions:
                self.list_of_actions.remove(action)

    @abstractmethod
    def set_possible_actions(self):
        pass
