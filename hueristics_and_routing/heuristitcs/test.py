import math
import time

import csv

import matplotlib.pyplot as plt
import numpy as np
import subprocess
# -----------------------  Random settings
rnd = np.random

# Global toggle for dynamism [UI setting?]
dynamic = False



#  meters
MAX_CLUSTER_DISTANCE = 4000

# no_buses=2
# no_passengers=5
# rnd.seed(1)

# Bus max capacity
max_bus_cap = 15

# How many stops from total 5000
break_count = 5000

# Max tolerable time difference between targeted arrival and actual arrival
max_lateness = 1000


