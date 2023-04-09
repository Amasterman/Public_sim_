![337452507_1190960121611328_2848777528685803948_n](https://user-images.githubusercontent.com/85699014/230694090-ba3e9993-46e9-4b57-a536-b7048ad388c7.png)

# Public*sim*

A Python based routing simulator. Takes the XML map data taken form OSM format maps and a matrix of times to reach each stop from another stop. This maxtrix was generated with a C++ based routing solver and imported into the simulator.
The sim will output a graph showing the vehicle routes as well as output the connections that the vehicles and passengers take. ~Will be added to log output soon~~
To run the simulator run the main.py file.
The run method acts as a selector for diffrent heuristics used to solve the routing problem.
validate_route takes any generated route and validates that it does not break any of the set requierments for the scenario
