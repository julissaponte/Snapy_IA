from juegoui import Juego
from constantes import DERECHA, IZQUIERDA, ARRIBA, ABAJO


class HillClimbing(Juego):
    def __init__(self, game_type):
        Juego.__init__(self, game_type)

    def calcular_heuristica(self, point):
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    def generar_camino(self):
        vecinos = []
        direcciones = [IZQUIERDA, DERECHA, ARRIBA, ABAJO]
        for direccion in direcciones:
            vecino = self.obtener_siguiente_cabeza(direccion)
            if not self.detectar_colision_random(vecino, 0):
                vecino.h = self.calcular_heuristica(vecino)
                vecinos.append((vecino, direccion))
        if vecinos:
            current_h = self.calcular_heuristica(self.head)
            vecino, direccion = min(vecinos, key=lambda x: x[0].h)
            if vecino.h < current_h:
                return direccion
        return None


class AStar(Juego):
    def __init__(self, game_type):
        Juego.__init__(self, game_type)
        self.open = [self.head]
        self.closed = []
        self.generar_camino()

    def calcular_heuristica(self, point):
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    def generar_camino(self):
        self.path = [self.head]
        self.closed = []
        self.open = [self.head]
        while self.open:
            actual = min(self.open, key=lambda x: x.f)
            self.open = [self.open[i] for i in range(len(self.open)) if not self.open[i] == actual]
            self.closed.append(actual)
            if actual == self.food:
                while actual.origen:
                    self.path.append(actual)
                    actual = actual.origen
                return
            actual.generar_vecinos()
            for vecino in actual.vecinos:
                if vecino not in self.obstacles and vecino not in self.snake:
                    g_temp = actual.g + 1
                    if vecino not in self.open and vecino not in self.closed:
                        vecino.h = self.calcular_heuristica(vecino)
                        vecino.g = g_temp
                        vecino.f = vecino.g + vecino.h
                        vecino.origen = actual
                        self.open.append(vecino)
                    else:
                        if vecino in self.open:
                            old_vecino = [x for x in self.open if x == vecino][0]
                            if old_vecino.g > g_temp:
                                old_vecino.h = self.calcular_heuristica(vecino)
                                old_vecino.g = g_temp
                                old_vecino.f = vecino.g + vecino.h
                                old_vecino.origen = actual

                        elif vecino in self.closed:
                            old_vecino = [x for x in self.closed if x == vecino][0]
                            if old_vecino.g > g_temp:
                                old_vecino.h = self.calcular_heuristica(vecino)
                                old_vecino.g = g_temp
                                old_vecino.f = vecino.g + vecino.h
                                old_vecino.origen = actual
                                self.closed = [self.closed[i] for i in range(len(self.closed)) if
                                               not self.closed[i] == old_vecino]
                                self.open.append(old_vecino)
        self.path = []