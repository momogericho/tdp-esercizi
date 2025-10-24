import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._model.buildGraph()
        num_nodi=self._model.getLenNodes()
        num_archi=self._model.getLenEdges()
        peso_max= self._model.getMaxPeso()
        peso_min=self._model.getMinPeso()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo è stato correttamente creato ed ha {num_nodi} nodi e {num_archi} archi"))
        self._view.txt_result.controls.append(ft.Text(f"I pesi degli archi vanno da un minimo di {peso_min} a un massimo di {peso_max}"))
        self._view.update()

    def handle_countedges(self, e):
        soglia=self.getSoglia()
        if soglia == -1:
            return
        self._model.conta_archi(soglia)
        len_archi_maggiori=self._model.lenArchiMaggiori()
        len_archi_minori=self._model.lenArchiMinori()
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso maggiore della soglia: {len_archi_maggiori}"))
        self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso minore della soglia: {len_archi_minori}"))

    def handle_search(self, e):
        sequenza_cromosomi=self._model.cercaCammino()
        if len(sequenza_cromosomi) == 0:
            self._view.txt_result3.controls.clear()
            self._view.txt_result3.controls.append(ft.Text(f"Non è stato trovato un percorso con queste caratteristiche"))
            return
        peso_cammino_massimo=self._model.getBestLunghezzaCammino()
        self._view.txt_result3.controls.clear()
        self._view.txt_result3.controls.append(ft.Text(f"Peso cammino massimo: {peso_cammino_massimo}"))
        for edge in sequenza_cromosomi:
            self._view.txt_result3.controls.append(ft.Text(f"{edge[0]} --> {edge[1]}: {edge[2]}"))

    def getSoglia(self):
        soglia=self._view.txt_name.value
        try:
            soglia = int(soglia)
        except ValueError:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text(f"Inserire nel valore di soglia un numero"))
            return -1
        peso_max = self._model.getMaxPeso()
        peso_min = self._model.getMinPeso()
        if soglia < peso_min:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(
                ft.Text(f"Inserire nel valore di soglia un numero maggiore o uguale della soglia minima {peso_min} "))
            return -1
        if soglia > peso_max:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(
                ft.Text(f"Inserire nel valore di soglia un numero minore o uguale della soglia massima {peso_max} "))
            return -1
        return soglia