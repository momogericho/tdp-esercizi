import copy

import networkx as nx


class Model:
    def __init__(self):
        self._grafo_geni= nx.DiGraph
        self._max_peso_arco is None
        self._min_peso_arco is None
        self._archi_maggiori_soglia = []
        self._archi_minori_soglia = []
        self._bestPercorso=[]
        self._bestLunghezzaCammino=0


    def buildGraph(self):
        self._grafo_geni.clear()
        lista_cromosomi= DAO.getAllCromosomi()
        self._grafo_geni.add_nodes_from(lista_cromosomi)
        lista_archi_pesati= DAO.getAllWeightedEdges()
        for edge in lista_archi_pesati:
            if edge[0] in lista_cromosomi and edge[1] in lista_cromosomi:
                self.calcolaMassimoeMinimo(edge[2])
                self._grafo_geni.add_edge(edge[0], edge[1], weight=edge[2])

    def conta_archi(self,soglia):
        edges= self._grafo_geni.edges
        self._archi_maggiori_soglia=[]
        self._archi_minori_soglia=[]
        for edge in edges:
            if self._grafo_geni[edge[0]][edge[1]]['weight'] > soglia:
                self._archi_maggiori_soglia.append(edge)
            if self._grafo_geni[edge[0]][edge[1]]['weight'] < soglia:
                self._archi_minori_soglia.append(edge)


    def cercaCammino(self):
        self._bestPercorso=[]
        self._bestLunghezzaCammino=0
        parziale=[]
        for edge in self._archi_maggiori_soglia:
            v0=edge[0]
            v1=edge[1]
            peso=self._grafo_geni[v0][v1]['weight']
            parziale.append((v0,v1,peso))
            self._ricorsione(parziale)
            parziale.pop()
        return self._bestPercorso

    def _ricorsione(self, parziale):
        peso_tot=self.calcolaPercorso(parziale)
        if peso_tot>self._bestLunghezzaCammino:
            self._bestLunghezzaCammino=peso_tot
            self._bestPercorso=copy.deepcopy(parziale)
        for edge in self._archi_maggiori_soglia:
            v0=edge[0]
            v1=edge[1]
            peso=self._grafo_geni[v0][v1]['weight']
            if parziale[-1][1]==v0:
               parziale.append((v0,v1,peso))
               self._ricorsione(parziale)
               parziale.pop()

    def calcolaPercorso(self,lista_peso):
        somma =0
        for edge in lista_peso:
            somma+=edge[2]
        return somma


    def calcolaMassimoeMinimo(self,peso):
        if self._max_peso_arco is None:
            self._max_peso_arco = peso
        if self._min_peso_arco is None:
            self._min_peso_arco = peso
        if self._min_peso_arco > peso:
            self._min_peso_arco = peso
        if self._max_peso_arco < peso:
            self._max_peso_arco = peso

    def getLenNodes(self):
        return len(self._grafo_geni.nodes)
    def getLenEdges(self):
        return len(self._grafo_geni.edges)
    def getMaxPeso(self):
        return self._max_peso_arco
    def getMinPeso(self):
        return self._min_peso_arco
    def lenArchiMaggiori(self):
        return len(self._archi_maggiori_soglia)
    def lenArchiMinori(self):
        return len(self._archi_minori_soglia)
    def getBestLunghezzaCammino(self):
        return self._bestLunghezzaCammino
