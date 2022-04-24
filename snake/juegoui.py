import random
import time
import pygame
import matplotlib.pyplot as plt
from constantes import ANCHO, ALTO, TAMANIO_BLOQUE, OBSTACULOS_LIMITE, AUTO_VELOCIDAD, \
    A_STAR_ALGORITMO, HILL_CLIMBING_ALGORITMO, BLANCO, ROJO, AZUL, MARRON, VERDE, DERECHA, IZQUIERDA, ARRIBA, ABAJO


class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.vecinos = []
        self.origen = None

    def __eq__(self, point):
        return self.__class__ == point.__class__ and self.x == point.x and self.y == point.y

    def plot(self, display, color):
        pygame.draw.rect(display, color, pygame.Rect(self.x, self.y, TAMANIO_BLOQUE, TAMANIO_BLOQUE))

    def obtener_direccion(self):
        if self.x == self.origen.x and self.y < self.origen.y:
            return ARRIBA
        elif self.x == self.origen.x and self.y > self.origen.y:
            return ABAJO
        elif self.x < self.origen.x and self.y == self.origen.y:
            return IZQUIERDA
        elif self.x > self.origen.x and self.y == self.origen.y:
            return DERECHA

    def generar_vecinos(self):
        if self.x > 0:
            self.vecinos.append(Punto(self.x - TAMANIO_BLOQUE, self.y))
        if self.y > 0:
            self.vecinos.append(Punto(self.x, self.y - TAMANIO_BLOQUE))
        if self.x < ANCHO - TAMANIO_BLOQUE:
            self.vecinos.append(Punto(self.x + TAMANIO_BLOQUE, self.y))
        if self.y < ALTO - TAMANIO_BLOQUE:
            self.vecinos.append(Punto(self.x, self.y + TAMANIO_BLOQUE))


class Juego:
    def __init__(self, game_type, width=ANCHO, height=ALTO):
        self.tipo_juego = game_type
        self.width = width
        self.height = height
        self.direction = ARRIBA
        self.head = Punto(self.width / 2, self.height / 2)
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
        pygame.display.set_caption('Snake Juego')

        # Obstaculos
        self.generar_obstaculos()
        # Comida
        self.generar_comida()

    def reset(self):
        self.direction = ARRIBA
        self.head = Punto(self.width / 2, self.height / 2)
        self.snake = [self.head]
        self.score = 0
        self.obstacles = []
        self.food = None
        self.elapsed_times = []
        self.scores = []
        self.generar_obstaculos()
        self.generar_comida()

    def generar_comida(self):
        x = random.randint(0, (self.width - TAMANIO_BLOQUE) // TAMANIO_BLOQUE) * TAMANIO_BLOQUE
        y = random.randint(0, (self.height - TAMANIO_BLOQUE) // TAMANIO_BLOQUE) * TAMANIO_BLOQUE
        self.food = Punto(x, y)
        if self.food in self.snake or self.food in self.obstacles:
            self.generar_comida()

    def generar_obstaculos(self):
        for _ in range(0, OBSTACULOS_LIMITE):
            x = random.randint(0, (self.width - TAMANIO_BLOQUE) // TAMANIO_BLOQUE) * TAMANIO_BLOQUE
            y = random.randint(0, (self.height - TAMANIO_BLOQUE) // TAMANIO_BLOQUE) * TAMANIO_BLOQUE
            obstacle = Punto(x, y)
            if obstacle not in self.snake:
                self.obstacles.append(obstacle)

    def obtener_siguiente_cabeza(self, direction):
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
        return Punto(x, y)

    def detectar_colision(self):
        if self.head.x > self.width - TAMANIO_BLOQUE or self.head.x < 0 or self.head.y > self.height - TAMANIO_BLOQUE or self.head.y < 0:
            return True
        if self.head in self.snake[1:]:
            return True
        if self.head in self.obstacles:
            return True

    def detectar_colision_random(self, point, start=1):
        if point.x > self.width - TAMANIO_BLOQUE or point.x < 0 or point.y > self.height - TAMANIO_BLOQUE or point.y < 0:
            return True
        if point in self.snake[start:]:
            return True
        if point in self.obstacles:
            return True

    def actualizar_ui(self):
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

    def generar_plot(self):
        total_time = 0
        quantity = 0
        for elapsed_time in self.elapsed_times:
            total_time += elapsed_time
            quantity = quantity + 1
        avg_time = total_time / quantity
        tt = "Tiempo total transcurrido: " + str(round(total_time, 3))
        at = "Tiempo promedio: " + str(round(avg_time, 3))

        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(self.scores, self.elapsed_times, label=self.tipo_juego)
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

    def guardar_datos_plot(self):
        actual = time.time()
        self.elapsed_times.append(actual - self.start)
        self.scores.append(self.score)
        self.start = time.time()

    def solo_uno(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.generar_plot()
                    pygame.quit()
                    quit()

            self.direction = self.generar_camino()
            if not self.direction:
                return self.score

            # Move snake
            self.head = self.obtener_siguiente_cabeza(self.direction)
            self.snake.insert(0, self.head)

            if self.detectar_colision():
                return self.score

            elif self.head == self.food:
                self.score += 1
                self.guardar_datos_plot()
                self.generar_comida()
            else:
                self.snake.pop()

            self.actualizar_ui()
            self.clock.tick(AUTO_VELOCIDAD)

    def multiple(self):
        while self.path:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.generar_plot()
                    pygame.quit()
                    quit()

            self.direction = self.path.pop(-1).obtener_direccion()
            self.head = self.obtener_siguiente_cabeza(self.direction)
            self.snake.insert(0, self.head)

            if self.detectar_colision():
                return self.score
            elif self.head == self.food:
                self.score += 1
                self.guardar_datos_plot()
                self.generar_comida()
                self.generar_camino()
            else:
                self.snake.pop()

            self.actualizar_ui()
            self.clock.tick(AUTO_VELOCIDAD)
        return self.score

    def main(self):
        if self.tipo_juego in HILL_CLIMBING_ALGORITMO:
            return self.solo_uno()
        elif self.tipo_juego in A_STAR_ALGORITMO:
            return self.multiple()
        else:
            raise Exception(f"Invalid algorithm: {self.tipo_juego}!")
