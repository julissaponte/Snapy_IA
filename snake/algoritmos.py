from juegoui import Game
from constantes import DERECHA, IZQUIERDA, ARRIBA, ABAJO


class HillClimbing(Game):
    def __init__(self, game_type):
        Game.__init__(self, game_type)

    def calcular_heuristica(self, point):
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    def generar_camino(self):
        vecinos = []
        direcciones = [IZQUIERDA, DERECHA, ARRIBA, ABAJO]
        for direccion in direcciones:
            vecino = self.get_next_head(direccion)
            if not self.detect_random_point_collision(vecino, 0):
                vecino.h = self.calcular_heuristica(vecino)
                vecinos.append((vecino, direccion))
        if vecinos:
            current_h = self.calcular_heuristica(self.head)
            vecino, direccion = min(vecinos, key=lambda x: x[0].h)
            if vecino.h < current_h:
                return direccion
        return None


class AStar(Game):
    def __init__(self, game_type):
        Game.__init__(self, game_type)
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
                while actual.origin:
                    self.path.append(actual)
                    actual = actual.origin
                return
            actual.generate_neighbors()
            for neighbor in actual.neighbors:
                if neighbor not in self.obstacles and neighbor not in self.snake:
                    g_temp = actual.g + 1
                    if neighbor not in self.open and neighbor not in self.closed:
                        neighbor.h = self.calcular_heuristica(neighbor)
                        neighbor.g = g_temp
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.origin = actual
                        self.open.append(neighbor)
                    else:
                        if neighbor in self.open:
                            old_neighbor = [x for x in self.open if x == neighbor][0]
                            if old_neighbor.g > g_temp:
                                old_neighbor.h = self.calcular_heuristica(neighbor)
                                old_neighbor.g = g_temp
                                old_neighbor.f = neighbor.g + neighbor.h
                                old_neighbor.origin = actual

                        elif neighbor in self.closed:
                            old_neighbor = [x for x in self.closed if x == neighbor][0]
                            if old_neighbor.g > g_temp:
                                old_neighbor.h = self.calcular_heuristica(neighbor)
                                old_neighbor.g = g_temp
                                old_neighbor.f = neighbor.g + neighbor.h
                                old_neighbor.origin = actual
                                self.closed = [self.closed[i] for i in range(len(self.closed)) if
                                               not self.closed[i] == old_neighbor]
                                self.open.append(old_neighbor)
        self.path = []