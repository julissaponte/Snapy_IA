from juegoui import Game
from constantes import DERECHA, IZQUIERDA, ARRIBA, ABAJO


class HillClimbing(Game):
    def __init__(self, game_type):
        Game.__init__(self, game_type)

    def calculate_h(self, point):
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    def generate_path(self):
        neighbors = []
        directions = [IZQUIERDA, DERECHA, ARRIBA, ABAJO]
        for direction in directions:
            neighbor = self.get_next_head(direction)
            if not self.detect_random_point_collision(neighbor, 0):
                neighbor.h = self.calculate_h(neighbor)
                neighbors.append((neighbor, direction))
        if neighbors:
            current_h = self.calculate_h(self.head)
            neighbor, direction = min(neighbors, key=lambda x: x[0].h)
            if neighbor.h < current_h:
                return direction
        return None


class AStar(Game):
    def __init__(self, game_type):
        Game.__init__(self, game_type)
        self.open = [self.head]
        self.closed = []

        self.generate_path()

    def calculate_h(self, point):
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    def generate_path(self):
        self.path = [self.head]
        self.closed = []
        self.open = [self.head]
        while self.open:
            current = min(self.open, key=lambda x: x.f)
            self.open = [self.open[i] for i in range(len(self.open)) if not self.open[i] == current]
            self.closed.append(current)
            if current == self.food:
                while current.origin:
                    self.path.append(current)
                    current = current.origin
                return
            current.generate_neighbors()
            for neighbor in current.neighbors:
                if neighbor not in self.obstacles and neighbor not in self.snake:
                    g_temp = current.g + 1
                    if neighbor not in self.open and neighbor not in self.closed:
                        neighbor.h = self.calculate_h(neighbor)
                        neighbor.g = g_temp
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.origin = current
                        self.open.append(neighbor)
                    else:
                        if neighbor in self.open:
                            old_neighbor = [x for x in self.open if x == neighbor][0]
                            if old_neighbor.g > g_temp:
                                old_neighbor.h = self.calculate_h(neighbor)
                                old_neighbor.g = g_temp
                                old_neighbor.f = neighbor.g + neighbor.h
                                old_neighbor.origin = current

                        elif neighbor in self.closed:
                            old_neighbor = [x for x in self.closed if x == neighbor][0]
                            if old_neighbor.g > g_temp:
                                old_neighbor.h = self.calculate_h(neighbor)
                                old_neighbor.g = g_temp
                                old_neighbor.f = neighbor.g + neighbor.h
                                old_neighbor.origin = current
                                self.closed = [self.closed[i] for i in range(len(self.closed)) if
                                               not self.closed[i] == old_neighbor]
                                self.open.append(old_neighbor)
        self.path = []