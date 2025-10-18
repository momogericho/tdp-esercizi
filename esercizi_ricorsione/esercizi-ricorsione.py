import copy
import time
from functools import lru_cache


# il fattoriale definito come N!=N*(N-1)!
#la compessità della funzione è di tipo o(N)
def fattoriale(N):
    if (N<=1 and N>=0):
        return 1
    elif N<0:
        print(f"Non si puo fare per un numero minore di zero")
        exit()
    else:
        return N*fattoriale(N-1)

#fibonacci con il caching ha complessità o(N)
@lru_cache
def fibonacci(N):
    if N<=1 and N>=0:
        return 1
    elif N<0:
        return 0
    else:
        return fibonacci(N-1) + fibonacci(N-2)


def anagramma(word):
    soluzioni= []
    parola= list(word)
    ricorsione_anagramma(parola,[],soluzioni)
    return soluzioni

def ricorsione_anagramma(rimanenti,parziale,soluzioni):
    if (len(rimanenti)<=0):
        if parziale not in soluzioni:
           soluzioni.append(copy.deepcopy(parziale))

    for char in rimanenti:
        parziale.append(char)
        nuovi_rimanenti=copy.deepcopy(rimanenti)
        nuovi_rimanenti.remove(char)
        ricorsione_anagramma(nuovi_rimanenti,parziale,soluzioni)
        parziale.remove(char)




if __name__ == "__main__":

    print(f"Se vuoi fare un operazione scrivi qualsiasi cosa, se non vuoi lascia vuoto o metti 0")

    flag_anagramma= bool(input(f"Vuoi fare gli anagrammi?   "))
    if (flag_anagramma):
        parola=input("Parola: ")
        start_time=time.time()
        anagrammi=anagramma(parola)
        end_time=time.time()
        print(f"Tutti gli anagrammi di {parola} sono {len(anagrammi)}")
        print(f"{anagrammi}")
        print(f"Il tempo impiegato per calcolare tutti gli anagrammi è di {end_time-start_time} secondi")


    flagRicorsioniFF=bool(input(f" Vuoi fare le interazioni per fibonacci e il fattoriale?  "))
    if flagRicorsioniFF:
        x = int(input(f"Inserire il numero intero di iterazioni dei cicli del fatt e del fib"))

        for i in range(x):
          start_time = time.time()
          fact = fattoriale(i)
          end_time = time.time()
          print(f"Il fattoriale di {i} è {fact}")
          print(f"Il tempo messo è {end_time - start_time}")

        for i in range(x):
          start_time = time.time()
          fib = fibonacci(i)
          end_time = time.time()
          print(f"Il fattoriale di {i} è {fib}")
          print(f"Il tempo messo è {end_time - start_time}")