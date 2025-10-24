import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        listYear=self._model.fillDD()
        for year in listYear:
            try:
                year=int(year)
            except ValueError:
                return
            if year >=1910 and year <=2014:
                self._view.ddyear.options.append(ft.DropdownOption(ft.Text(str(year),value=year,on_click=self.fillShapes)))
        self._view.update_page()

    def fillShapes(self,e):
        year = e.value
        if year is None:
            return
        listShapes=self._model.fillShape(year)
        if listShapes is None:
            return
        for shape in listShapes:
            self._view.ddshape.options.append(ft.DropdownOption(str(ft.Text(shape))),value=shape,on_click=self._model.setShape)
        self._view.update_page()

    def handle_graph(self, e):
        lista_nodo_pesi=self._model.buildGraph()
        caso_mancato_anno=f"Scegli l'anno per continuare"
        caso_mancata_forma=f"Scegli la forma per continuare"
        if lista_nodo_pesi is caso_mancato_anno:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(caso_mancato_anno,color=yellow))
            self._view.update_page()
            return
        if lista_nodo_pesi is caso_mancata_forma:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(caso_mancata_forma,color=yellow))
            self._view.update_page()
            return

        len_nodi=self._model.getLenNodes()
        len_archi=self._model.getLenEdges()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {len_nodi} nodi e {len_archi} archi"))
        for nodo_pesi in lista_nodo_pesi:
            self._view.txt_result.controls.append(ft.Text(f"Nodo {nodo_pesi[0]}, somma pesi tra archi {nodo_pesi[1]}"))
        self._view.update_page()

    def handle_path(self, e):
        lista_tappe=[]
        lista_tappe=self._model.buildPath()
        lunghezza_percorso=len(lista_tappe)
        if lunghezza_percorso is None:
            self._view.txtOut2.controls.clear()
            self._view.txtOut2.controls.append(ft.Text(f"Non esiste un percorso semplice che massimizza la distanza geodesica tra due stati"))
            return
        stato_sorgente=self._model.printById(lista_tappe[0].getNodoSorgente())
        stato_destinazione=self._model.printStateById(lista_tappe[-1].getNodoDestinazione())
        distanza_geodesica=self._model.calcolaDistanzaDueStati(stato_sorgente,stato_destinazione)
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"Il percorso trovato con massima distanza ha lunghezza {lunghezza_percorso} inizia da {stato_sorgente} e termina a {stato_destinazione} con distanza {distanza_geodesica} km"))
        for tappa in lista_tappe:
            self._view.txt_result.controls.append(ft.Text(tappa.printDetails()))
        self._view.update_page()


    #############
    #--HELPERS--#
    #############
    def getSelectedYear(self):
        return self._model.getSelectedYear()

    def getSelectedShape(self):
        return self._model.getSelectedShape()

