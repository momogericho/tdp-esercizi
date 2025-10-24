from dataclasses import dataclass

@dataclass
class State():
    id: str
    name: str
    capital: str
    lat: float
    lng: float
    area: int
    population : int
    neighbors: str

    def printDetails(self):
        return f"{self.name} ({self.id})"
    def getLng(self):
        return self.lng
    def getLat(self):
        return self.lat