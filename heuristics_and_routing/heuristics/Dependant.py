"""
Meta class for dependant. A dependant is an agent that is affected by the dependency. They have the ability to have
a weight associated with the dependencies. Additionally, they have a relationship matrix for the interdependencies
both linear and non-linear.

"""
from abc import ABCMeta, abstractmethod


class Dependant(metaclass=ABCMeta):
    pass
