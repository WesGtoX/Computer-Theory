# -29.310803,-50.854238   –   Cachoeira do Caracol (Canela – RS)
# -26.392177,-49.355748   –   Cachoeira do Salto Grande (Corupa – SC)
# -25.690346,-54.440839   –   Cachoeira do Itambé (São Benedito das Areias – SP)
# -21.290040,-47.145398   –   Cachoeira do Tabuleiro (Conceição do Mato Dentro – MG)
# -19.088765,-43.551510   –   Cachoeira Conde D’eu (Sumidouro – RJ)
# -22.139910,-42.654060   –   Cachoeira da Fumaça (Alegre – ES)
# -20.624641,-41.602874   –   Cachoeira Boca da Onça (Bodoquena – MS)
# -20.740040,-56.734793   –   Cachoeira Véu da Noiva (Chapada dos Guimarães – MT)
# -13.856665,-47.454317   –   Cachoeira Santa Bárbara (Cavalcante – GO)
# -13.539699,-47.492756   –   Cachoeira do Tororó (Santa Maria – DF)
# -15.983273,-47.834249   –   Cachoeira do Formiga (Mateiros – TO)

from math import radians, cos, sin, asin, sqrt

# Formula de Haversine
def haversine( latA, lonA, latB, lonB ):
    # Raio da Terra em Metros
    r = 6371000

    # Converte coordenadas de graus para radianos
    lon1, lat1, lon2, lat2 = map(radians, [lonA, latA, lonB, latB])

    # Formula de Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    hav = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    d = 2 * r * asin(sqrt(hav))

    return d


dist = 0;
lat0 = 0;
lon0 = 0;

with open("coord.csv") as arq:

    for i, amostra in enumerate(arq):

        lat,lon = amostra.strip('\n').split(',')
        lat,lon = float(lat), float(lon)

        if( i > 0 ):
            dist = haversine( lat, lon, lat0, lon0 );
            print("[Amostra %d] Latitude: %f, Longitude: %f, Distancia: %f Km" % (i, lat, lon, dist/1000))
        else:
            print("[Amostra %d] Latitude: %f, Longitude: %f" % (i, lat, lon))

        lat0 = lat;
        lon0 = lon;