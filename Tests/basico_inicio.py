# Creación del entorno

# Carga Librerías

import random # Para los números aleatorios
import pygame
import time


# Inicializa pygame

pygame.font.init()

def dibuja_cuadrados(win):
    pygame.draw.rect(win, (0, 255, 0), (50, 50, 100, 100), 3)

def main():
    # Establecer el tamaño de la ventana y lo mete en una variable
    win = pygame.display.set_mode((1600,1000))

    # Establecer el título de la ventana
    pygame.display.set_caption("Ventana de Test1")

    # La pinta de color blanco el fondo
    win.fill((255,255,255))

    # Ejecución de programa
    # Quitar las señales a las partes que quiero ejecutar

    # Cuadrado verde claro
    pygame.draw.rect(win, (233, 252, 193), (50, 50, 100, 100), 0)

    # Cuadrado rojo claro
    pygame.draw.rect(win, (238, 36, 48), (50, 150, 100, 100), 0)

    # Cuadrado verde oscuro
    pygame.draw.rect(win, (41, 158, 41), (50, 250, 100, 100), 0)

    # Cuadrado marron
    pygame.draw.rect(win, (201, 135, 58), (50, 350, 100, 100), 0)

    # Ejemplo de como mantener un programa corriendo hasta que cambias una variable.

    # Defines la variable
    run = True

 

    # Mientras no la cambies a False, sigue corriendo en loop
    while run:

        # Esto es necesario para que puedas cerrar la ventana creada pulsando en la X de arriba
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # si actualizo datos, puedos pintarlos en este loop
        
        pygame.display.update()


main()
pygame.quit()

# --------------------------------------------------------------

