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
    # Set variables to print Distance Matrix
    distance_locals = []
    go_to_local = destiny['local'].tolist()
    col = ['local']
    col += go_to_local

    matrix = pd.DataFrame(columns=col)

    for i in matrix:
        if i != 'local':
            distance_locals.append(i)
    print(distance_locals)

    # Loop to generate all distances and print Distance Matrix
    distances_matrix = []
    for index, l_origin in origin.iterrows():
        info_distance = []
        for index, l_destiny in destiny.iterrows():
            query = gmaps.distance_matrix(l_origin['latlong'], l_destiny['latlong'])
            distance = query['rows'][0]['elements'][0]['distance']['value']

            info_distance.append(distance)

        distances_matrix.append(info_distance)

        info_temp = [l_origin['local']]
        info_temp.extend(info_distance)

        temp = pd.DataFrame([info_temp], columns=col)
        matrix = matrix.append(temp, ignore_index=True)

        print(info_temp)

    # Save Distance Matrix on CSV file
    matrix.to_csv('waterfall_file.csv', encoding='utf-8', index=False)

    # Set 'local' as line index
    matrix = matrix.set_index('local')

#Read Distance Matrix CSV,
# waterfall_file = pd.read_csv('waterfall_file.csv')

#Set 'local' as line index and print
# waterfall_file = waterfall_file.set_index('local')
# waterfall_file

distance_locals = [
    'Cachoeira do Caracol', 'Cachoeira do Salto Grande', 'Cataratas do Iguacu', 'Cachoeira do Itambe',
    'Cachoeira do Tabuleiro', 'Cachoeira Conde Deu', 'Cachoeira da Fumaca', 'Cachoeira Boca da Onca',
    'Cachoeira Veu da Noiva', 'Cachoeira Santa Barbara', 'Cachoeira do Tororo', 'Cachoeira do Formiga']


distances_matrix = [[0, 640811, 949945, 1401670, 1890739, 1683095, 1876670, 1584813, 2389494, 2412956, 2086137, 2970082],
                    [655244, 0, 755519, 821714, 1310782, 1103139, 1296713, 1308429, 1809537, 1832999, 1506180, 2390125],
                    [950309, 755565, 0, 1076559, 1686875, 1639653, 1833228, 860642, 1876380, 1899842, 1573023, 2456968],
                    [1402527, 823157, 1075251, 0, 647488, 703937, 848643, 1176039, 1049281, 1072743, 745924, 1629869],
                    [1889850, 1310480, 1684642, 666973, 0, 608990, 526142, 1758524, 1052001, 1075463, 748644, 1426938],
                    [1672630, 1093260, 1627625, 698885, 609927, 0, 277678, 1815932, 1429570, 1453032, 1126213, 1930277],
                    [1867680, 1288309, 1822675, 843948, 518337, 277465, 0, 2010982, 1418695, 1442157, 1115338, 1919403],
                    [1585461, 1309184, 856924, 1191968, 1761486, 1827306, 2020880, 0, 1656970, 1680432, 1358071, 2234997],
                    [2387230, 1807860, 1872348, 1047209, 1053176, 1429588, 1441565, 1656723, 0, 41690, 338379, 664616],
                    [2410692, 1831321, 1895810, 1070671, 1076638, 1453050, 1465027, 1680185, 41690, 0, 361841, 688078],
                    [2083529, 1504158, 1568647, 743508, 749474, 1125887, 1137864, 1371121, 349531, 372993, 0, 930119],
                    [2967940, 2388569, 2453058, 1627919, 1419406, 1929356, 1895871, 2234899, 664607, 688069, 919089, 0]]


def get_best_route():
    dist_best_route = []
    best_route_name = []
    index_best_route = [0]
    i = 0
    control = -1

    while len(index_best_route) != 12:
        minus_route = -1
        for k in range(len(distances_matrix[i])):
            if k != i and minus_route == -1 and k not in index_best_route:
                minus_route = distances_matrix[i][k]
                control = k
            if minus_route != -1 and minus_route > distances_matrix[i][k] and k != i and k not in index_best_route:
                minus_route = distances_matrix[i][k]
                control = k

        index_best_route.append(control)
        dist_best_route.append(minus_route)
        i = control


    for i in range(len(index_best_route)):
        best_route_name.append(distance_locals[index_best_route[i]])


    waterfall_distance = 0
    for i in range(len(dist_best_route)):
        waterfall_distance = waterfall_distance + dist_best_route[i]

    print(dist_best_route)
    print(best_route_name)

    i = 0
    for i in range(len(dist_best_route)):
        print(best_route_name[i] + " -- " + str(dist_best_route[i]) + " --> " + best_route_name[i+1])
        i+=1

    # return dist_best_route


get_best_route()
