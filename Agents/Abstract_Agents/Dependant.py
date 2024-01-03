"""
Meta class for dependant. A dependant is an agent that is affected by the dependency. They have the ability to have
a weight associated with the dependencies. Additionally, they have a relationship matrix for the interdependencies
both linear and non-linear.

"""
from abc import ABCMeta

from Agents.Abstract_Agents.Agent import Agent


class Dependant(metaclass=ABCMeta, Agent):

    def __init__(self, pos_x, pos_y):
        """Constructor method"""
        super().__init__(pos_x, pos_y)

    def set_dependency_weight(self):
        pass

    def set_interdependency_function(self):
        pass

    def set_lin_dependency(self):
        """ Want this one to set basic X=Y relationship"""

    def set_exp_dependency(self):
        """ Want this one to set basic X=Y^2 relationship"""

    def set_log_dependency(self):
        """ Want this one to set basic X=log(Y) relationship"""

    def set_normal_dependency(self):
        """ Want this one to set X=(1/sd*√(2π))*e^-1/2(x-mean/sd) relationship"""

    def set_sigmoid_dependency(self):
        """ Want this one to set X=(1/(1+e^-x)) relationship"""

