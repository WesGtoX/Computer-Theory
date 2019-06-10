import networkx as nx
import statistics
import matplotlib.pyplot as plt
from queue import PriorityQueue
import math


class Grafo(object):

    def __init__(self, grafo_dict={}):
        self.grafo_dict = grafo_dict

    def vertices(self):
        return list(self.grafo_dict.keys())

    def arestas(self):
        return self.gerar_arestas()

    def adicionar_vertice(self, vertice):
        if vertice not in self.grafo_dict:
            self.grafo_dict[vertice] = []

    def adicionar_aresta(self, bidirecional=False, *aresta):
        (vertice1, vertice2, custo) = aresta
        self.adicionar_vertice(vertice1)
        self.adicionar_vertice(vertice2)
        self.add_aresta_sem_repeticao(vertice1, vertice2, custo)
        if bidirecional:
            self.add_aresta_sem_repeticao(vertice2, vertice1, custo)

    def add_aresta_sem_repeticao(self, vertice1, vertice2, custo):
        lista_vertice1 = self.grafo_dict[vertice1]
        for i, (vertice, _) in enumerate(lista_vertice1):
            if vertice == vertice2:
                lista_vertice1[i] = (vertice2, custo)
                break
        else:
            lista_vertice1.append((vertice2, custo))

    def custo_direto(self, vertice1, vertice2):
        lista_vertice1 = self.grafo_dict[vertice1]
        for (vertice, custo) in lista_vertice1:
            if vertice == vertice2:
                return custo
        else:
            return math.inf

    def gerar_arestas(self):
        aresta = []
        for vertice in self.grafo_dict:
            for (vizinho, custo) in self.grafo_dict[vertice]:
                if (vizinho, vertice) not in aresta:
                    aresta.append(((vertice, vizinho, custo)))
        return aresta

    def __str__(self):
        return 'Vertices: {0}\nArestas: {1}'.format(sorted(self.vertices()), sorted(self.arestas()))


def dijkstra(grafo, root):
    queue = PriorityQueue()     # lista de prioridades
    caminho = {}        # dicionario com o caminho e o custo total
    for vertice in grafo.vertices():
        if vertice == root:
            caminho[vertice] = [[], 0]      # custo 0 para o root
        else:
            caminho[vertice] = [[], math.inf]        # custo infinito para os demais
        queue.put((caminho[vertice][1], vertice))       # adiciona todas na lista de prioridade (maior prioridade = menor custo
    vertices_remanescentes = list(grafo.vertices())     # lista de vertices nao visitados
    for i in range(len(grafo.vertices())):
        prioritario = queue.get()[1]        # vertice prioritario da lista
        vertices_remanescentes.remove(prioritario)      # remove da lista de nao visitados
        for vertice in vertices_remanescentes:      # para cada vertice nao visitado
            menor_prioritario = caminho[prioritario][1]     # menor custo ate o vertice prioritario
            custo = grafo.custo_direto(prioritario, vertice)        # custo de prioritario ate vertice
            menor_custo_prioritario = caminho[vertice][1]       # menor custo ate o vertice
            if menor_prioritario + custo < menor_custo_prioritario:     # o caminho ate o vertice pelo prioritario e menos custoso que o melhor ate entao
                caminho[vertice][1] = menor_prioritario + custo     # atualiza o custo
                caminho[vertice][0] = caminho[prioritario][0] + [prioritario]       # atualiza o caminho
                queue.queue.remove((menor_custo_prioritario, vertice))      # atualiza a prioridade do vertice na lista de prioridade
                queue.put((caminho[vertice][1], vertice))
    return caminho

def converter_caminho_str(caminho):
    caminho_str = []
    vertices = sorted(caminho.keys())
    for vertice in vertices:
        custo = caminho[vertice][1]
        if custo == 0:
            continue
        string = ' --- '.join(caminho[vertice][0]) + ' --- ' + vertice
        caminho_str.append(string.upper() + ' = custo: ' + str(custo))
    return '\n'.join(caminho_str)

def prim(grafo, root):
    vertice = [root]        # lista dos vertices a partir do qual buscamos as arestas
    vertice_selecionada = []        # lista com as arestas selecionadas
    peso = 0        # peso do minimum spanning tree
    vertices_remanescentes = list(grafo.vertices())     # lista com os vertices destunos da busca
    vertices_remanescentes.remove(root)     # o root é o ponto de partida, então sai da lista
    for i in range(len(vertices_remanescentes)):
        custo_minimo = math.inf      # inicializa o custo minimo como infinito
        vertice_a, vertice_b = None, None       # vertices candidatos para a aresta selecionada
        for vertice_1 in vertice:       # para cada vertice na lista de busca de origem
            for vertice_2 in vertices_remanescentes:        # busca os vertices que anida nao estao no grafo final
                custo = grafo.custo_direto(vertice_1, vertice_2)        # calcula o custo da aresta
                if custo < custo_minimo:        # se for menor que o minimo ate entao, atualiza os dados
                    vertice_a = vertice_1
                    vertice_b = vertice_2
                    custo_minimo = custo
        if custo_minimo < math.inf:      # depois de todas as buscas, se o custo é finito:
            vertice_selecionada.append((vertice_a, vertice_b, custo_minimo))        # adcionamos a aresta de vertice_a a vertice_b na solucao
            vertice.append(vertice_b)       # vertice_b agora sera nova origem de busca
            vertices_remanescentes.remove(vertice_b)        # vertice_b nao mais sera o destino de busca, pois ja consta na solucao
            peso += custo_minimo        # atualiza o peso
    return vertice_selecionada, peso        # retorna a lista de arestas selecionadas com o peso total

def imprimir_grafo(grafo, salvar_png=False):
    nx_grafo = nx.Graph()
    custos = []
    for (vertice_a, vertice_b, custo) in grafo.arestas():
        nx_grafo.add_edge(vertice_a, vertice_b, custo=custo)
        custos.append(custo)

    pos = nx.spring_layout(nx_grafo)        # posicao para todos os nos

    custo_medio = statistics.mean(custos)

    elarge = [(u, v) for (u, v, d) in nx_grafo.edges(data=True) if d['custo'] > custo_medio]
    esmall = [(u, v) for (u, v, d) in nx_grafo.edges(data=True) if d['custo'] <= custo_medio]

    # nos
    nx.draw_networkx_nodes(nx_grafo, pos, node_size=700)

    # arestas
    nx.draw_networkx_edges(nx_grafo, pos, edgelist=elarge, width=4)
    nx.draw_networkx_edges(nx_grafo, pos, edgelist=esmall, width=4, alpha=0.5, edge_color='b', style='dashed')

    # labels
    nx.draw_networkx_labels(nx_grafo, pos, font_size=20, font_family='sans-serif')
    # nx.draw_networkx_edge_labels(nx_grafo, pos)

    plt.axis('off')
    if salvar_png:
        plt.savefig("grafo.png")        # salva como png
    plt.show()      # plota o grafo

def carregar_grafo_letra():
    grafo = [
        ('a', 'b', 0.640826),('a', 'c', 0.949966),('a', 'd', 0.1369275),('a', 'e', 0.1863630),('a', 'f', 0.1646214),('a', 'g', 0.1837410),('a', 'h', 0.1584884),('a', 'i', 0.2359051),('a', 'j', 0.2382511),('a', 'k', 0.2055704),('a', 'l', 0.2939706),
        ('b', 'a', 0.640654),('b', 'c', 0.755502),('b', 'd', 0.816306),('b', 'e', 0.1310661),('b', 'f', 0.1093244),('b', 'g', 0.1284441),('b', 'h', 0.1308287),('b', 'i', 0.1806081),('b', 'j', 0.1829541),('b', 'k', 0.1502734),('b', 'l', 0.2386736),
        ('c', 'a', 0.944047),('c', 'b', 0.753159),('c', 'd', 0.1064706),('c', 'e', 0.1675028),('c', 'f', 0.1617897),('c', 'g', 0.1809094),('c', 'h', 0.858237),('c', 'i', 0.1861038),('c', 'j', 0.1884498),('c', 'k', 0.1557692),('c', 'l', 0.2441693),
        ('d', 'a', 0.1448976),('d', 'b', 0.830328),('d', 'c', 0.1067247),('d', 'e', 0.647491),('d', 'f', 0.696594),('d', 'g', 0.848246),('d', 'h', 0.1176037),('d', 'i', 0.1045810),('d', 'j', 0.1069270),('d', 'k', 0.742463),('d', 'l', 0.1626465),
        ('e', 'a', 0.1929128),('e', 'b', 0.1310480),('e', 'c', 0.1676631),('e', 'd', 0.647054),('e', 'f', 0.601648),('e', 'g', 0.526142),('e', 'h', 0.1758513),('e', 'i', 0.1051998),('e', 'j', 0.1075458),('e', 'k', 0.748652),('e', 'l', 0.1424885),
        ('f', 'a', 0.1711914),('f', 'b', 0.1093266),('f', 'c', 0.1619624),('f', 'd', 0.698887),('f', 'e', 0.609938),('f', 'g', 0.275292),('f', 'h', 0.1815937),('f', 'i', 0.1429575),('f', 'j', 0.1453035),('f', 'k', 0.1126228),('f', 'l', 0.1930347),
        ('g', 'a', 0.1906972),('g', 'b', 0.1288323),('g', 'c', 0.1814682),('g', 'd', 0.842088),('g', 'e', 0.518337),('g', 'f', 0.277465),('g', 'h', 0.2010994),('g', 'i', 0.1440625),('g', 'j', 0.1464085),('g', 'k', 0.1137278),('g', 'l', 0.1941397),
        ('h', 'a', 0.1581596),('h', 'b', 0.1309179),('h', 'c', 0.856920),('h', 'd', 0.1191969),('h', 'e', 0.1762419),('h', 'f', 0.1817398),('h', 'g', 0.2008595),('h', 'i', 0.1656214),('h', 'j', 0.1679674),('h', 'k', 0.1357317),('h', 'l', 0.2234308),
        ('i', 'a', 0.2426321),('i', 'b', 0.1807672),('i', 'c', 0.1863441),('i', 'd', 0.1047016),('i', 'e', 0.1053173),('i', 'f', 0.1422245),('i', 'g', 0.1441572),('i', 'h', 0.1655558),('i', 'j', 0.41700),('i', 'k', 0.338377),('i', 'l', 0.664622),
        ('j', 'a', 0.2449781),('j', 'b', 0.1831132),('j', 'c', 0.1886901),('j', 'd', 0.1070476),('j', 'e', 0.1076633),('j', 'f', 0.1445705),('j', 'g', 0.1465032),('j', 'h', 0.1679018),('j', 'i', 0.41700),('j', 'k', 0.361837),('j', 'l', 0.688082),
        ('k', 'a', 0.2122615),('k', 'b', 0.1503967),('k', 'c', 0.1559735),('k', 'd', 0.743311),('k', 'e', 0.749468),('k', 'f', 0.1118539),('k', 'g', 0.1137867),('k', 'h', 0.1362428),('k', 'i', 0.341998),('k', 'j', 0.365458),('k', 'l', 0.922653),
        ('l', 'a', 0.3007055),('l', 'b', 0.2388407),('l', 'c', 0.2444175),('l', 'd', 0.1627751),('l', 'e', 0.1426507),('l', 'f', 0.1922036),('l', 'g', 0.1941363),('l', 'h', 0.2233759),('l', 'i', 0.664609),('l', 'j', 0.688069),('l', 'k', 0.919112)
    ]
    menu_escolha = "a – Cachoeira do Caracol\nb – Cachoeira do Salto Grande\nc – Cataratas do Iguacu\n" \
                   "d – Cachoeira do Itambe\ne – Cachoeira do Tabuleiro\nf – Cachoeira Conde Deu\n" \
                   "g – Cachoeira da Fumaca\nh – Cachoeira Boca da Onca\ni – Cachoeira Veu da Noiva\n" \
                   "j – Cachoeira Santa Barbara\nk – Cachoeira do Tororo\nl – Cachoeira do Formiga"
    return grafo, menu_escolha

def carregar_grafo_nome():
    grafo = [
        ('Cachoeira do Caracol', 'Cachoeira do Salto Grande', 0.640826),('Cachoeira do Caracol', 'Cataratas do Iguacu', 0.949966),('Cachoeira do Caracol', 'Cachoeira do Itambe', 0.1369275),('Cachoeira do Caracol', 'Cachoeira do Tabuleiro', 0.1863630),('Cachoeira do Caracol', 'Cachoeira Conde Deu', 0.1646214),('Cachoeira do Caracol', 'Cachoeira da Fumaca', 0.1837410),('Cachoeira do Caracol', 'Cachoeira Boca da Onca', 0.1584884),('Cachoeira do Caracol', 'Cachoeira Veu da Noiva', 0.2359051),('Cachoeira do Caracol', 'Cachoeira Santa Barbara', 0.2382511),('Cachoeira do Caracol', 'Cachoeira do Tororo', 0.2055704),('Cachoeira do Caracol', 'Cachoeira do Formiga', 0.2939706),
        ('Cachoeira do Salto Grande', 'Cachoeira do Caracol', 0.640654),('Cachoeira do Salto Grande', 'Cataratas do Iguacu', 0.755502),('Cachoeira do Salto Grande', 'Cachoeira do Itambe', 0.816306),('Cachoeira do Salto Grande', 'Cachoeira do Tabuleiro', 0.1310661),('Cachoeira do Salto Grande', 'Cachoeira Conde Deu', 0.1093244),('Cachoeira do Salto Grande', 'Cachoeira da Fumaca', 0.1284441),('Cachoeira do Salto Grande', 'Cachoeira Boca da Onca', 0.1308287),('Cachoeira do Salto Grande', 'Cachoeira Veu da Noiva', 0.1806081),('Cachoeira do Salto Grande', 'Cachoeira Santa Barbara', 0.1829541),('Cachoeira do Salto Grande', 'Cachoeira do Tororo', 0.1502734),('Cachoeira do Salto Grande', 'Cachoeira do Formiga', 0.2386736),
        ('Cataratas do Iguacu', 'Cachoeira do Caracol', 0.944047),('Cataratas do Iguacu', 'Cachoeira do Salto Grande', 0.753159),('Cataratas do Iguacu', 'Cachoeira do Itambe', 0.1064706),('Cataratas do Iguacu', 'Cachoeira do Tabuleiro', 0.1675028),('Cataratas do Iguacu', 'Cachoeira Conde Deu', 0.1617897),('Cataratas do Iguacu', 'Cachoeira da Fumaca', 0.1809094),('Cataratas do Iguacu', 'Cachoeira Boca da Onca', 0.858237),('Cataratas do Iguacu', 'Cachoeira Veu da Noiva', 0.1861038),('Cataratas do Iguacu', 'Cachoeira Santa Barbara', 0.1884498),('Cataratas do Iguacu', 'Cachoeira do Tororo', 0.1557692),('Cataratas do Iguacu', 'Cachoeira do Formiga', 0.2441693),
        ('Cachoeira do Itambe', 'Cachoeira do Caracol', 0.1448976),('Cachoeira do Itambe', 'Cachoeira do Salto Grande', 0.830328),('Cachoeira do Itambe', 'Cataratas do Iguacu', 0.1067247),('Cachoeira do Itambe', 'Cachoeira do Tabuleiro', 0.647491),('Cachoeira do Itambe', 'Cachoeira Conde Deu', 0.696594),('Cachoeira do Itambe', 'Cachoeira da Fumaca', 0.848246),('Cachoeira do Itambe', 'Cachoeira Boca da Onca', 0.1176037),('Cachoeira do Itambe', 'Cachoeira Veu da Noiva', 0.1045810),('Cachoeira do Itambe', 'Cachoeira Santa Barbara', 0.1069270),('Cachoeira do Itambe', 'Cachoeira do Tororo', 0.742463),('Cachoeira do Itambe', 'Cachoeira do Formiga', 0.1626465),
        ('Cachoeira do Tabuleiro', 'Cachoeira do Caracol', 0.1929128),('Cachoeira do Tabuleiro', 'Cachoeira do Salto Grande', 0.1310480),('Cachoeira do Tabuleiro', 'Cataratas do Iguacu', 0.1676631),('Cachoeira do Tabuleiro', 'Cachoeira do Itambe', 0.647054),('Cachoeira do Tabuleiro', 'Cachoeira Conde Deu', 0.601648),('Cachoeira do Tabuleiro', 'Cachoeira da Fumaca', 0.526142),('Cachoeira do Tabuleiro', 'Cachoeira Boca da Onca', 0.1758513),('Cachoeira do Tabuleiro', 'Cachoeira Veu da Noiva', 0.1051998),('Cachoeira do Tabuleiro', 'Cachoeira Santa Barbara', 0.1075458),('Cachoeira do Tabuleiro', 'Cachoeira do Tororo', 0.748652),('Cachoeira do Tabuleiro', 'Cachoeira do Formiga', 0.1424885),
        ('Cachoeira Conde Deu', 'Cachoeira do Caracol', 0.1711914),('Cachoeira Conde Deu', 'Cachoeira do Salto Grande', 0.1093266),('Cachoeira Conde Deu', 'Cataratas do Iguacu', 0.1619624),('Cachoeira Conde Deu', 'Cachoeira do Itambe', 0.698887),('Cachoeira Conde Deu', 'Cachoeira do Tabuleiro', 0.609938),('Cachoeira Conde Deu', 'Cachoeira da Fumaca', 0.275292),('Cachoeira Conde Deu', 'Cachoeira Boca da Onca', 0.1815937),('Cachoeira Conde Deu', 'Cachoeira Veu da Noiva', 0.1429575),('Cachoeira Conde Deu', 'Cachoeira Santa Barbara', 0.1453035),('Cachoeira Conde Deu', 'Cachoeira do Tororo', 0.1126228),('Cachoeira Conde Deu', 'Cachoeira do Formiga', 0.1930347),
        ('Cachoeira da Fumaca', 'Cachoeira do Caracol', 0.1906972),('Cachoeira da Fumaca', 'Cachoeira do Salto Grande', 0.1288323),('Cachoeira da Fumaca', 'Cataratas do Iguacu', 0.1814682),('Cachoeira da Fumaca', 'Cachoeira do Itambe', 0.842088),('Cachoeira da Fumaca', 'Cachoeira do Tabuleiro', 0.518337),('Cachoeira da Fumaca', 'Cachoeira Conde Deu', 0.277465),('Cachoeira da Fumaca', 'Cachoeira Boca da Onca', 0.2010994),('Cachoeira da Fumaca', 'Cachoeira Veu da Noiva', 0.1440625),('Cachoeira da Fumaca', 'Cachoeira Santa Barbara', 0.1464085),('Cachoeira da Fumaca', 'Cachoeira do Tororo', 0.1137278),('Cachoeira da Fumaca', 'Cachoeira do Formiga', 0.1941397),
        ('Cachoeira Boca da Onca', 'Cachoeira do Caracol', 0.1581596),('Cachoeira Boca da Onca', 'Cachoeira do Salto Grande', 0.1309179),('Cachoeira Boca da Onca', 'Cataratas do Iguacu', 0.856920),('Cachoeira Boca da Onca', 'Cachoeira do Itambe', 0.1191969),('Cachoeira Boca da Onca', 'Cachoeira do Tabuleiro', 0.1762419),('Cachoeira Boca da Onca', 'Cachoeira Conde Deu', 0.1817398),('Cachoeira Boca da Onca', 'Cachoeira da Fumaca', 0.2008595),('Cachoeira Boca da Onca', 'Cachoeira Veu da Noiva', 0.1656214),('Cachoeira Boca da Onca', 'Cachoeira Santa Barbara', 0.1679674),('Cachoeira Boca da Onca', 'Cachoeira do Tororo', 0.1357317),('Cachoeira Boca da Onca', 'Cachoeira do Formiga', 0.2234308),
        ('Cachoeira Veu da Noiva', 'Cachoeira do Caracol', 0.2426321),('Cachoeira Veu da Noiva', 'Cachoeira do Salto Grande', 0.1807672),('Cachoeira Veu da Noiva', 'Cataratas do Iguacu', 0.1863441),('Cachoeira Veu da Noiva', 'Cachoeira do Itambe', 0.1047016),('Cachoeira Veu da Noiva', 'Cachoeira do Tabuleiro', 0.1053173),('Cachoeira Veu da Noiva', 'Cachoeira Conde Deu', 0.1422245),('Cachoeira Veu da Noiva', 'Cachoeira da Fumaca', 0.1441572),('Cachoeira Veu da Noiva', 'Cachoeira Boca da Onca', 0.1655558),('Cachoeira Veu da Noiva', 'Cachoeira Santa Barbara', 0.41700),('Cachoeira Veu da Noiva', 'Cachoeira do Tororo', 0.338377),('Cachoeira Veu da Noiva', 'Cachoeira do Formiga', 0.664622),
        ('Cachoeira Santa Barbara', 'Cachoeira do Caracol', 0.2449781),('Cachoeira Santa Barbara', 'Cachoeira do Salto Grande', 0.1831132),('Cachoeira Santa Barbara', 'Cataratas do Iguacu', 0.1886901),('Cachoeira Santa Barbara', 'Cachoeira do Itambe', 0.1070476),('Cachoeira Santa Barbara', 'Cachoeira do Tabuleiro', 0.1076633),('Cachoeira Santa Barbara', 'Cachoeira Conde Deu', 0.1445705),('Cachoeira Santa Barbara', 'Cachoeira da Fumaca', 0.1465032),('Cachoeira Santa Barbara', 'Cachoeira Boca da Onca', 0.1679018),('Cachoeira Santa Barbara', 'Cachoeira Veu da Noiva', 0.41700),('Cachoeira Santa Barbara', 'Cachoeira do Tororo', 0.361837),('Cachoeira Santa Barbara', 'Cachoeira do Formiga', 0.688082),
        ('Cachoeira do Tororo', 'Cachoeira do Caracol', 0.2122615),('Cachoeira do Tororo', 'Cachoeira do Salto Grande', 0.1503967),('Cachoeira do Tororo', 'Cataratas do Iguacu', 0.1559735),('Cachoeira do Tororo', 'Cachoeira do Itambe', 0.743311),('Cachoeira do Tororo', 'Cachoeira do Tabuleiro', 0.749468),('Cachoeira do Tororo', 'Cachoeira Conde Deu', 0.1118539),('Cachoeira do Tororo', 'Cachoeira da Fumaca', 0.1137867),('Cachoeira do Tororo', 'Cachoeira Boca da Onca', 0.1362428),('Cachoeira do Tororo', 'Cachoeira Veu da Noiva', 0.341998),('Cachoeira do Tororo', 'Cachoeira Santa Barbara', 0.365458),('Cachoeira do Tororo', 'Cachoeira do Formiga', 0.922653),
        ('Cachoeira do Formiga', 'Cachoeira do Caracol', 0.3007055),('Cachoeira do Formiga', 'Cachoeira do Salto Grande', 0.2388407),('Cachoeira do Formiga', 'Cataratas do Iguacu', 0.2444175),('Cachoeira do Formiga', 'Cachoeira do Itambe', 0.1627751),('Cachoeira do Formiga', 'Cachoeira do Tabuleiro', 0.1426507),('Cachoeira do Formiga', 'Cachoeira Conde Deu', 0.1922036),('Cachoeira do Formiga', 'Cachoeira da Fumaca', 0.1941363),('Cachoeira do Formiga', 'Cachoeira Boca da Onca', 0.2233759),('Cachoeira do Formiga', 'Cachoeira Veu da Noiva', 0.664609),('Cachoeira do Formiga', 'Cachoeira Santa Barbara', 0.688069),('Cachoeira do Formiga', 'Cachoeira do Tororo', 0.919112)
    ]
    waterfall_lista = [
        'Cachoeira do Caracol', 'Cachoeira do Salto Grande', 'Cataratas do Iguacu', 'Cachoeira do Itambe',
        'Cachoeira do Tabuleiro', 'Cachoeira Conde Deu', 'Cachoeira da Fumaca', 'Cachoeira Boca da Onca',
        'Cachoeira Veu da Noiva', 'Cachoeira Santa Barbara', 'Cachoeira do Tororo', 'Cachoeira do Formiga'
    ]
    menu_escolha = " 1 – Cachoeira do Caracol\n 2 – Cachoeira do Salto Grande\n 3 – Cataratas do Iguacu\n" \
                   " 4 – Cachoeira do Itambe\n 5 – Cachoeira do Tabuleiro\n 6 – Cachoeira Conde Deu\n" \
                   " 7 – Cachoeira da Fumaca\n 8 – Cachoeira Boca da Onca\n 9 – Cachoeira Veu da Noiva\n" \
                   "10 – Cachoeira Santa Barbara\n11 – Cachoeira do Tororo\n12 – Cachoeira do Formiga"
    return grafo, waterfall_lista, menu_escolha


if __name__ == '__main__':
    grafo_dict = Grafo({})

    ar = int(input("Deseja o grafo por nome das cachoeiras ou letra:\n0 - Letra\n1 - Nome\n==> "))

    if ar == 0:         # letra
        arestas, menu_escolha = carregar_grafo_letra()
        print(menu_escolha)
        index = input("Informa o a cidade que deseja sair:\n==> ")
        root = index.lower()
    elif ar == 1:       # nome
        arestas, waterfall, menu_escolha = carregar_grafo_nome()
        print(menu_escolha)
        index = int(input("Informa o a cidade que deseja sair:\n==> "))
        root = waterfall[index - 1]
    else:
        arestas = []
        root = 0
        menu_escolha = ""
        print("ERROR")
    print("----------")

    bidirect = int(input("Esse grafo é bidirectional:\n0 - Não\n1 - Sim\n==> "))
    bidirecional = False if bidirect == 0 else True

    for aresta in arestas:
        grafo_dict.adicionar_aresta(bidirecional, *aresta)

    grafo_prim = Grafo({})

    prim, peso = prim(grafo_dict, root)     # retorna as arestas e o peso
    for aresta in prim:
        grafo_prim.adicionar_aresta(bidirecional, *aresta)

    print("\nGrafo original:\n%s" % grafo_dict)
    print("----------")
    print("Caminhos mais curtos desde o vertice '" + root.upper() + "': \n%s" % converter_caminho_str(dijkstra(grafo_dict, root)))
    print("----------")
    print('Minima Arvore Abrangente (Peso Final = %s):\n%s' % (peso, grafo_prim))

    # imprimir_grafo(grafo_dict)
    # imprimir_grafo(grafo_prim)
