#prendere i fie presenti in input_raw, formattarli,comporli
import os

def initializer():
    cartella_input_raw=None
    cartella_input_formattati=None

    for cartella,sottocartelle,files in os.walk(os.getcwd()):
        print(f"{os.getcwd()}")
        print(f"cartella: {cartella}")
        print(f"sottocartelle: {sottocartelle}")
        print(f"files: {files}")
        print()
        if cartella=={os.getcwd()}:
            print(f"cartella raw: {cartella}")

#funzione di formattazione
def format_input():
    pass


if __name__ == "__main__":
    initializer()