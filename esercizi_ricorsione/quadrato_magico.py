import copy


class quadratoMagico:

    def __init__(self):
        self._soluzioni=[]



    def quadrato_magico(self,N):
        numero_magico= N*(N-1)/2
        parziale=[]
        rimanenti=[]
        for i in range(1,N*N):
           rimanenti.append(i)
        for numero in rimanenti:
            parziale.append(numero)
            rimanenti_nuova=copy.deepcopy(rimanenti)
            self.ricorsione(N,numero_magico,parziale,rimanenti_nuova)
            parziale.pop()


    def ricorsione(self,N,numero_magico,parziale,rimanenti):
        if len(parziale)==N*N:
            if self.soluzione_ammissibile(parziale):
                self._soluzioni.append(copy.deepcopy(parziale))
            return
        else:
            for numero in rimanenti:
                if self.iterazione_ammissibile(numero,parziale):
                   parziale.append(numero)
                   rimanenti_nuova = copy.deepcopy(rimanenti)
                   rimanenti_nuova.remove(numero)
                   self.ricorsione(numero_magico, parziale, rimanenti_nuova)
                   parziale.pop()

    def soluzione_ammissibile(self,parziale,N):
        for i in range(0,N*N) :
            row=i%N
        #controllo sulle righe
        #controllo sulle colonne
        #controllo sulla diagonale ascendente/
        #controllo sulla diagonale discendente\

    def iterazione_ammissibile(self,numero,parziale):
        pass
