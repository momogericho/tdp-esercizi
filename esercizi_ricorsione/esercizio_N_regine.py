import copy
import os
from time import sleep

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def risoluzione_N_regine(N):
    #inizializzazione
    soluzioni=[]
    #ricorsione
    ricorsione_regine(0,[],N,soluzioni)
    print("Sono arrivato fino a qua")
    # ritornare i risultati
    #for soluzione in soluzioni:
    #    print_matrice(soluzione)

def ricorsione_regine(row,parziale,N,soluzioni):
    if row >= N:
        if parziale not in soluzioni and soluzione_ammissibile(parziale):
            soluzione=copy.deepcopy(parziale)
            soluzioni.append(soluzione)
            print_matrice(soluzione)

    else:
        for col in range(N):
            regina_attuale=[row,col]
            if check_ammissibilità_regina_attuale(regina_attuale,parziale):
               parziale.append([row,col])
               row+=1
               ricorsione_regine(row,parziale,N,soluzioni)
               row-=1
               parziale.pop()


def soluzione_ammissibile(parziale):
    pos_row=set()
    pos_col=set()
    pos_diag_disc=set()
    pos_diag_asc=set()
    for regina in parziale:
        #condizione righe
        pos_row.add(regina[0])
        #condizione colonne
        pos_col.add(regina[1])
        #condizione diagonale discendente\
        diag_disc=regina[0]-regina[1]
        if diag_disc<0:
            diag_disc=diag_disc*(-1)
        pos_diag_disc.add(diag_disc)
        #condizione diagonale/
        pos_diag_asc.add(regina[0]+regina[1])
    flag_ammissibile= ((len(pos_row)==len(pos_col))and(len(pos_diag_asc)==len(pos_diag_disc))and(len(pos_row)==len(pos_diag_asc))and(len(pos_col)==len(parziale)))
    return flag_ammissibile

def check_ammissibilità_regina_attuale(regina_attuale,parziale):
    for regina in parziale:
        print(f"regina attuale: ({regina_attuale[0]},{regina_attuale[1]}) --- regina: ({regina[0]},{regina[1]})")
        #condizione righe-
        if regina_attuale[0]==regina[0]:
            return False
        #condizione colonne|
        if regina_attuale[1]==regina[1]:
            return False
        #condizione diagonale\
        diag_disc=regina[0]-regina[1]
        diag_disc_attuale=regina_attuale[0]-regina_attuale[1]
        if diag_disc==diag_disc_attuale or diag_disc==(-diag_disc_attuale):
            return False
        #condizione diagonale/
        diag_asc=regina[0]+regina[1]
        diag_asc_attuale=regina_attuale[0]+regina_attuale[1]
        if diag_asc==diag_asc_attuale:
            return False
    return True

def print_matrice(soluzione):
    #creo una matrice N*N con la lunghezza della soluzione,costruisco la matrice iterativamente,aggiungendo la regina se serve
    N=len(soluzione)
    for row in range(N):
        for col in range(N):
            if [row,col] in soluzione :
                print(f"[R:{row},{col}]",end="")
            else:
                if ((row+col)%2==0):
                    print(f"[   ]",end="")
                else:
                    print(f"[***]",end="")
        print("",end='\n')

def starter():
    lun = input(f"Inserisci la larghezza della matrice su cui risolvere il problema delle N regine: ")
    try:
        lun = int(lun)
        risoluzione_N_regine(lun)
    except ValueError:
        cls()
        print(f"Puoi inserire solamente numeri interi per indicare la larghezza della matrice")
        sleep(1)
        starter()

if __name__ == '__main__':
    starter()