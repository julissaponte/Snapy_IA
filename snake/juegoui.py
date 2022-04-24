import random
import time
import pygame
import matplotlib.pyplot as plt
from constantes import ANCHO, ALTO, TAMANIO_BLOQUE, OBSTACULOS_LIMITE, AUTO_VELOCIDAD, \
    A_STAR_ALGORITMO, HILL_CLIMBING_ALGORITMO, BLANCO, ROJO, AZUL, MARRON, VERDE, DERECHA, IZQUIERDA, ARRIBA, ABAJO


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.origin = None

    def __eq__(self, point):
        return self.__class__ == point.__class__ and self.x == point.x and self.y == point.y

    def plot(self, display, color):
        pygame.draw.rect(display, color, pygame.Rect(self.x, self.y, TAMANIO_BLOQUE, TAMANIO_BLOQUE))

    def get_direction(self):
        if self.x == self.origin.x and self.y < self.origin.y:
            return ARRIBA
        elif self.x == self.origin.x and self.y > self.origin.y:
            return ABAJO
        elif self.x < self.origin.x and self.y == self.origin.y:
            return IZQUIERDA
        elif self.x > self.origin.x and self.y == self.origin.y:
            return DERECHA

    def generate_neighbors(self):
        if self.x > 0:
            self.neighbors.append(Point(self.x - TAMANIO_BLOQUE, self.y))
        if self.y > 0:
            self.neighbors.append(Point(self.x, self.y - TAMANIO_BLOQUE))
        if self.x < ANCHO - TAMANIO_BLOQUE:
            self.neighbors.append(Point(self.x + TAMANIO_BLOQUE, self.y))
        if self.y < ALTO - TAMANIO_BLOQUE:
            self.neighbors.append(Point(self.x, self.y + TAMANIO_BLOQUE))


class Game:
    def __init__(self, game_type, width=ANCHO, height=ALTO):
        self.game_type = game_type
        self.width = width
        self.height = height
        self.direction = ARRIBA
        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [self.head]
        self.score = 0
        self.obstacles = []
        self.food = None
        self.path = []
        self.start = time.time()
        self.elapsed_times = []
        self.scores = []

        self.display = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont('arial', 25)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Snake Game')

        # Obstaculos
        self.generate_obstacles()
        # Comida
        self.generate_food()

    def reset(self):
        self.direction = ARRIBA
        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [self.head]
        self.score = 0
        self.obstacles = []
        self.food = None
        self.elapsed_times = []
        self.scores = []
        self.generate_obstacles()
        self.generate_food()

    def generate_food(self):
        x = random.randint(0, (self.width - TAMANIO_BLOQUE) // TAMANIO_BLOQUE) * TAMANIO_BLOQUE
        y = random.randint(0, (self.height - TAMANIO_BLOQUE) // TAMANIO_BLOQUE) * TAMANIO_BLOQUE
        self.food = Point(x, y)
        if self.food in self.snake or self.food in self.obstacles:
            self.generate_food()

    def generate_obstacles(self):
        for _ in range(0, OBSTACULOS_LIMITE):
            x = random.randint(0, (self.width - TAMANIO_BLOQUE) // TAMANIO_BLOQUE) * TAMANIO_BLOQUE
            y = random.randint(0, (self.height - TAMANIO_BLOQUE) // TAMANIO_BLOQUE) * TAMANIO_BLOQUE
            obstacle = Point(x, y)
            if obstacle not in self.snake:
                self.obstacles.append(obstacle)

    def get_next_head(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == DERECHA:
            x += TAMANIO_BLOQUE
        elif direction == IZQUIERDA:
            x -= TAMANIO_BLOQUE
        elif direction == ABAJO:
            y += TAMANIO_BLOQUE
        elif direction == ARRIBA:
            y -= TAMANIO_BLOQUE
        return Point(x, y)

    def detect_collision(self):
        if self.head.x > self.width - TAMANIO_BLOQUE or self.head.x < 0 or self.head.y > self.height - TAMANIO_BLOQUE or self.head.y < 0:
            return True
        if self.head in self.snake[1:]:
            return True
        if self.head in self.obstacles:
            return True

    def detect_random_point_collision(self, point, start=1):
        if point.x > self.width - TAMANIO_BLOQUE or point.x < 0 or point.y > self.height - TAMANIO_BLOQUE or point.y < 0:
            return True
        if point in self.snake[start:]:
            return True
        if point in self.obstacles:
            return True

    def update_ui(self):
        self.display.fill(VERDE)
        for point in self.snake:
            point.plot(self.display, AZUL)
        self.head.plot(self.display, BLANCO)
        for point in self.obstacles:
            point.plot(self.display, MARRON)
        self.food.plot(self.display, ROJO)
        text = self.font.render("Score: " + str(self.score), True, BLANCO)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def generar_camino(self):
        pass

    def generate_plot(self):
        total_time = 0
        quantity = 0
        for elapsed_time in self.elapsed_times:
            total_time += elapsed_time
            quantity = quantity + 1
        avg_time = total_time / quantity
        tt = "Tiempo total transcurrido: " + str(round(total_time, 3))
        at = "Tiempo promedio: " + str(round(avg_time, 3))

        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(self.scores, self.elapsed_times, label=self.game_type)
        ax.set_title("Gráfico del tiempo que tarda el algoritmo en aumentar su puntaje")
        ax.set_xlabel("Puntaje")
        ax.set_ylabel("Tiempo en (s)")

        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height
        ax.legend()
        ax.text(0.5 * (left + right), 0.5 * (bottom + top), tt,
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes)
        ax.text(0.5 * (left + right), 0.6 * (bottom + top), at,
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes)
        plt.show()

    def save_plot_data(self):
        actual = time.time()
        self.elapsed_times.append(actual - self.start)
        self.scores.append(self.score)
        self.start = time.time()

    def single_step_traversal(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.generate_plot()
                    pygame.quit()
                    quit()

            self.direction = self.generar_camino()
            if not self.direction:
                return self.score

            # Move snake
            self.head = self.get_next_head(self.direction)
            self.snake.insert(0, self.head)

            if self.detect_collision():
                return self.score

            elif self.head == self.food:
                self.score += 1
                self.save_plot_data()
                self.generate_food()
            else:
                self.snake.pop()

            self.update_ui()
            self.clock.tick(AUTO_VELOCIDAD)

    def multi_step_traversal(self):
        while self.path:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.generate_plot()
                    pygame.quit()
                    quit()

            self.direction = self.path.pop(-1).get_direction()
            self.head = self.get_next_head(self.direction)
            self.snake.insert(0, self.head)

            if self.detect_collision():
                return self.score
            elif self.head == self.food:
                self.score += 1
                self.save_plot_data()
                self.generate_food()
                self.generar_camino()
            else:
                self.snake.pop()

            self.update_ui()
            self.clock.tick(AUTO_VELOCIDAD)
        return self.score

    def main(self):
        if self.game_type in HILL_CLIMBING_ALGORITMO:
            return self.single_step_traversal()
        elif self.game_type in A_STAR_ALGORITMO:
            return self.multi_step_traversal()
        else:
            raise Exception(f"Invalid algorithm: {self.game_type}!")
