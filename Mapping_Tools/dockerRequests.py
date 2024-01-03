import requests
import csv

# Open and read the coordinates from the input file
f = open("../Files/In/XML_to_TXT_OUT.txt")
coords = f.read()
f.close()

# Test print of server request
#print('http://127.0.0.1:5000/route/v1/driving', coords)

# Send request to the server and save response as r
r = requests.get("http://127.0.0.1:5000/table/v1/driving/" + coords)

# Format output into res
res = r.json()
durations = []

# Get durations from the results
durations = res["durations"]

# print(durations)

# Write the results to file
c = open('route_durations.CSV', "w+")
XML_out_writer = csv.writer(c, delimiter=',', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
for i in range(0, len(res["durations"])):
    XML_out_writer.writerow(res["durations"][i])

c.close()