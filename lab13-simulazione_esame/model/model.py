import copy

from database.DAO import DAO
from geopy.distance import geodesic
import networkx as nx
from model import *

class Model:
    def __init__(self):
        self._selectedYear = None
        self._selectedShape = None
        self._idMapStates = {}
        self._sommaPesiArchi={}
        self._ufoGraph= nx.Graph()
        self._percorsoMigliore= ()
        self._distanzaMigliore= 0

    def buildGraph(self):
        db = DAO()
        nodeList= db.getNodes()
        for state in nodeList:
            self._idMapStates[state["id"]] = state
            self._sommaPesiArchi[state] = 0
        self._ufoGraph.add_nodes_from(nodeList)
        if self._selectedYear is None:
            return f"Scegli l'anno per continuare"
            #scrivere qualcosa a terminale riguardo scegliere l'anno
        if self._selectedShape is None:
            return f"Scegli la forma per continuare"
            #scrivere qualcosa a terminale riguardo scegliere la forma

        edgeList= db.getWeightedEdges(self._selectedShape, self._selectedYear, self._idMapStates)
        for edge in edgeList:
            if self._idMapStates.get(edge[0].id) is not None and self._idMapStates.get(edge[1].id) is not None:
                self._ufoGraph.add_edge(edge[0],edge[1],weight=edge[2])
                self._sommaPesiArchi[edge[0]]+=edge[2]
                self._sommaPesiArchi[edge[1]]+=edge[2]
        list_nodo_pesi=[]
        for nodo in self._ufoGraph.nodes():
            list_nodo_pesi.append(nodo.id,self._sommaPesiArchi[nodo])
        return list_nodo_pesi

    def buildPath(self):
        self._percorsoMigliore=[]
        percorso_migliore_tappa=[]
        self._distanzaMigliore=0
        parziale=[]
        rimanenti=self._ufoGraph.nodes()
        ultimo_peso=0
        for stato in rimanenti:
            parziale.append(stato)
            rimanenti_nuova=copy.deepcopy(rimanenti)
            rimanenti_nuova.remove(stato)
            self._ricorsione(parziale,rimanenti_nuova,stato,ultimo_peso)
            parziale.pop()
        for i in len(self._percorsoMigliore)-2:
            nodo_sorg=self._percorsoMigliore[i]
            nodo_dest=self._percorsoMigliore[i+1]
            peso_arco=self._ufoGraph[nodo_sorg][nodo_dest]["weight"]
            dist_geod=self.calcolaDistanzaDueStati(nodo_sorg,nodo_dest)
            tappa=Tappa(nodo_sorg.id,nodo_dest.id,peso_arco,dist_geod)
            percorso_migliore_tappa.append(tappa)
        return percorso_migliore_tappa

    def _ricorsione(self,parziale,rimanenti,nodo_sorgente,ultimo_peso):
        nuova_distanza=self.calcolaDistanzaDueStati(nodo_sorgente,parziale[-1])
        if nuova_distanza>self._distanzaMigliore:
            self._distanzaMigliore=nuova_distanza
            self._percorsoMigliore=copy.deepcopy(parziale)
        for stato in rimanenti:
            if self._ufoGraph[parziale[-1]][stato]["weight"]>ultimo_peso:
                ultimo_peso=self._ufoGraph[parziale[-1]][stato]["weight"]
                parziale.append(stato)
                rimanenti_nuova = copy.deepcopy(rimanenti)
                rimanenti_nuova.remove(stato)
                self._ricorsione(parziale, rimanenti_nuova, stato, ultimo_peso)
                parziale.pop()

    def printById(self,id_states):
        stato=self._idMapStates[id_states]
        return stato.printDetails()

    def calcolaDistanzaDueStati(self,stato_sorgente,stato_destinazione):
        lat_sorg=stato_sorgente.getLat()
        lat_dest=stato_destinazione.getLat()
        lng_dest=stato_destinazione.getLng()
        lng_sorg=stato_sorgente.getLng()
        coord_sorg=(lat_sorg,lng_sorg)
        coord_dest=(lat_dest,lng_dest)
        distance=geodesic(coord_sorg,coord_dest).km
        return distance

    def fillShape(self, year):
        self._selectedYear = year
        db = DAO()
        return db.fillShapes(year)

    def fillYear(self):
        db=DAO()
        return db.fillYears()



    #--Helpers--#
    def setShape(self,e):
        self._selectedShape=e.value
    def getSelectedYear(self):
        return self._selectedYear
    def getSelectedShape(self):
        return self._selectedShape
    def getLenNodes(self):
        return len(self._ufoGraph.nodes())
    def getLenEdges(self):
        return len(self._ufoGraph.edges())