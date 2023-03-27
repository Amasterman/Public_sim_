import math
import time

import csv

import matplotlib.pyplot as plt
import numpy as np
import subprocess
# -----------------------  Random settings
rnd = np.random
rnd.seed(1)

# Global toggle for dynamism [UI setting?]
dynamic = False

# Area of longitude and latitude of the greater Southampton area [Better way to define?]
minlat = 50.8255000
minlon = -1.6263000
maxlat = 51.0142000
maxlon = -1.0873000

no_buses=2
no_passengers=4

# Bus max capacity
max_bus_cap = 15

# How many stops from total 5000
break_count = 300

# Max tolerable time difference between targeted arrival and actual arrival
max_lateness = 1000


