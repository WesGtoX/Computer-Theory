import googlemaps
import pandas as pd

gmaps = googlemaps.Client(key='AIzaSyDO7h3u-XM5WvK0Sm3SmDRcPxFBFnk5bwQ')

origin = pd.read_csv('locals.csv')
destiny = pd.read_csv('locals.csv')

col = ['id_origin', 'l_origin', 'id_destiny', 'l_destiny', 'distance']
matrix = pd.DataFrame(columns=col)

for index, l_origin in origin.iterrows():
    for index, l_destiny in destiny.iterrows():
        query = gmaps.distance_matrix(l_origin['latlong'], l_destiny['latlong'])

        distance = query['rows'][0]['elements'][0]['distance']['value']

        info_temp = [l_origin['id'], l_origin['local'],l_destiny['id'], l_destiny['local'],distance]

        temp = pd.DataFrame([info_temp], columns=col)
        matrix = matrix.append(temp, ignore_index=True)

        print(info_temp)

        # tag = str(l_origin['id']) + " " + l_origin['name'] + " --> " + str(l_destiny['id']) + " " + l_destiny['name']
        # print(tag, query['rows'][0]['elements'][0]['distance']['value'])

matrix.to_csv('waterfall_file.csv', encoding='utf-8', index=False)
