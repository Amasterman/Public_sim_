"""
Meta class for agents (For those unfamiliar with python these are the equivalent of interfaces, they cant be 
instantiated and must be inherited by other classes). In this case the


"""
from abc import ABCMeta, abstractmethod


class Agent(metaclass=ABCMeta):
    pass