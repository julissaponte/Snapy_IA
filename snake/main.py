import sys
import pygame
from algoritmos import HillClimbing, AStar


def obtener_clase_juego(game_type):
    return {
        'hill_climbing': HillClimbing,
        'a_star': AStar
    }.get(game_type)


if __name__ == '__main__':
    print('''
    Escribe el numero del algoritmo a elegir:
    1) A Star
    2) Hill Climbing
     ''')
    tipo_juego = ''
    try:
        numero_elegido = input()
        numero_elegido = int(numero_elegido)
        if numero_elegido == 1:
            tipo_juego = 'a_star'
        else:
            tipo_juego = 'hill_climbing'
    except IndexError:
        tipo_juego = 'a_star'

    pygame.init()
    clase_juego = obtener_clase_juego(tipo_juego)
    juego = clase_juego(tipo_juego)
    puntaje = juego.main()
    pygame.quit()
    sys.exit()
