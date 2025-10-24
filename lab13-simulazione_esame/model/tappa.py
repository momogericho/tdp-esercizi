from dataclasses import dataclass
@dataclass
class Tappa:
    nodo_sorgente: str
    nodo_destinazione: str
    peso_arco: int
    distanza_geodesica: float

    def getNodoSorgente(self):
        return self.nodo_sorgente
    def getNodoDestinazione(self):
        return self.nodo_destinazione
    def getPesoArco(self):
        return self.peso_arco
    def getDistanza_geodesica(self):
        return self.distanza_geodesica
    def printDetails(self):
        return f"{self.nodo_sorgente} -> {self.nodo_destinazione} , weight: {self.peso_arco} , distance: {self.distanza_geodesica}"