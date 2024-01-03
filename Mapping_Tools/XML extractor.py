import csv
import xml.etree.ElementTree as ET


# Write parameters to target CSV file
def writeLineToCsv(ref, name, lat, long, local_ref, network, operator, shelter, bench, tactile_paving, wheelchair,
                   departure_board
                   , lit, bins, covered, passenger_information_display, pole, flag, kerb, traffic_sign, advertising,
                   layer,
                   street, crossing):
    with open('../Files/In/XML_to_CSV_OUT.CSV', mode='a') as XML_OUT:
        XML_out_writer = csv.writer(XML_OUT, delimiter=',', lineterminator='\n', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)

        XML_out_writer.writerow(
            [ref, name, lat, long, local_ref, network, operator, shelter, bench, tactile_paving, wheelchair,
             departure_board, lit, bins, covered, passenger_information_display, pole, flag, kerb,
             traffic_sign, advertising, layer, street, crossing])
    XML_OUT.close()


# initialize the csv file by writing the headers
def initCSV():
    c = open('../Files/In/XML_to_CSV_OUT.CSV', "w+")
    XML_out_writer = csv.writer(c, delimiter=',', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    XML_out_writer.writerow(['ref', 'name', 'lat', 'long', 'local_ref', 'network', 'operator', 'shelter',
                             'bench', 'tactile_paving', 'wheelchair', 'departure_board', 'lit', 'bin', 'covered',
                             'passenger_information_display', 'pole', 'flag', 'kerb', 'traffic_sign', 'advertising',
                             'layer', 'street', 'crossing'])
    c.close()


# initialize text file
def initTXT():
    c = open('../Files/In/XML_to_TXT_OUT.txt', "w+")
    c.write(" ")
    c.close()


# Write to text file
def writeTXT(lat, long):
    c = open('../Files/In/XML_to_TXT_OUT.txt', "a")
    out = long + "," + lat + ";"
    c.write(out)
    c.close()


# Parse the XML as a tree
tree = ET.parse('Southampton Area Map OPM')
root = tree.getroot()

# Init bus stops
bus_stops = []

# init files
initCSV()
initTXT()

# Search all nodes
for node in root.findall('node'):

    # get all the tags for node
    tags = node.findall('tag')

    # Check through the tags
    for tag in tags:
        if tag is not None:
            # Save all bus stops
            if tag.attrib['v'] == "bus_stop" and tag.attrib['k'] == "highway":
                bus_stops.append(node)

for node in bus_stops:
    # Clear all tags and initialize as None. This is to prevent the csv file writing wrong
    tags = node.findall('tag')
    name = None
    local_ref = None
    network = None
    operator = None
    shelter = None
    bench = None
    tactile_paving = None
    wheelchair = None
    departure_board = None
    lit = None
    bins = None
    covered = None
    passenger_information_display = None
    pole = None
    flag = None
    kerb = None
    traffic_sign = None
    advertising = None
    layer = None
    street = None
    crossing = None

    # Check through all tags and save their values
    for tag in tags:
        if tag.attrib['k'] == "name":
            name = tag.attrib['v']

        if tag.attrib['k'] == "ref":
            ref = tag.attrib['v']

        if tag.attrib['k'] == "local_ref":
            local_ref = tag.attrib['v']

        if tag.attrib['k'] == "network":
            network = tag.attrib['v']

        if tag.attrib['k'] == "operator":
            operator = tag.attrib['v']

        if tag.attrib['k'] == "shelter":
            shelter = tag.attrib['v']

        if tag.attrib['k'] == "bench":
            bench = tag.attrib['v']

        if tag.attrib['k'] == "tactile_paving":
            tactile_paving = tag.attrib['v']

        if tag.attrib['k'] == "wheelchair":
            wheelchair = tag.attrib['v']

        if tag.attrib['k'] == "departure_board":
            departure_board = tag.attrib['v']

        if tag.attrib['k'] == "lit":
            lit = tag.attrib['v']

        if tag.attrib['k'] == "bin":
            bins = tag.attrib['v']

        if tag.attrib['k'] == "covered":
            covered = tag.attrib['v']

        if tag.attrib['k'] == "passenger_information_display":
            passenger_information_display = tag.attrib['v']

        if tag.attrib['k'] == "pole":
            pole = tag.attrib['v']

        if tag.attrib['k'] == "flag":
            flag = tag.attrib['v']

        if tag.attrib['k'] == "kerb":
            kerb = tag.attrib['v']

        if tag.attrib['k'] == "traffic_sign":
            traffic_sign = tag.attrib['v']

        if tag.attrib['k'] == "advertising":
            advertising = tag.attrib['v']

        if tag.attrib['k'] == "layer":
            layer = tag.attrib['v']

        if tag.attrib['k'] == "naptan:Street":
            street = tag.attrib['v']

        if tag.attrib['k'] == "naptan:Crossing":
            crossing = tag.attrib['v']

    # Write the tag data for each stop to the csv
    writeLineToCsv(node.attrib['id'], name, node.attrib['lat'], node.attrib['lon'], local_ref, network, operator,
                   shelter,
                   bench, tactile_paving, wheelchair, departure_board, lit, bins, covered,
                   passenger_information_display, pole,
                   kerb, flag, traffic_sign, advertising, layer, street, crossing)

    # Write just the latitude and longitude to a txt file indexed the same as the tags
    writeTXT(node.attrib['lat'], node.attrib['lon'])
