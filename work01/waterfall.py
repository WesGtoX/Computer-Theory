# import Google Maps and Pandas library
import googlemaps
# import config as config
import pandas as pd
import pprint as pp

def distance_matrix():
    # Set the Google Maps Key
    gmaps = googlemaps.Client(key=config.maps_apikey)

    # Import Origin and Destiny locals
    origin = pd.read_csv('locals.csv')
    destiny = pd.read_csv('locals.csv')

    # Set variables to print Distance Matrix
    go_to_local = destiny['local'].tolist()
    col = ['local']
    col += go_to_local

    matrix = pd.DataFrame(columns=col)

    # Loop to generate all distances and print Distance Matrix
    for index, l_origin in origin.iterrows():
        info_distance = []
        for index, l_destiny in destiny.iterrows():
            query = gmaps.distance_matrix(l_origin['latlong'], l_destiny['latlong'])
            distance = query['rows'][0]['elements'][0]['distance']['value']

            info_distance.append(distance)

        info_temp = [l_origin['local']]
        info_temp.extend(info_distance)

        temp = pd.DataFrame([info_temp], columns=col)
        matrix = matrix.append(temp, ignore_index=True)

        print(info_temp)

    # Save Distance Matrix on CSV file
    matrix.to_csv('waterfall_file.csv', encoding='utf-8', index=False)

    # Set 'local' as line index
    matrix = matrix.set_index('local')

# Read Distance Matrix CSV,
# waterfall_file = pd.read_csv('waterfall_file.csv')

# Set 'local' as line index and print
# waterfall_file = waterfall_file.set_index('local')
# waterfall_file


#                 Caracol,        SaltoGrande,    Iguacu,
# Caracol,        0,              640811,         949940,
# SaltoGrande,    655244,         0,              755514,
# Iguacu,         950303,         755556,         0,


distanceMatrix = [[0, 64, 94],
                   [65,0,75],
                   [95, 76, 0]]

for i in distanceMatrix:
    print(i)