# Creación del entorno

# Carga Librerías

import random # Para los números aleatorios
import pygame
import time


# Inicializa pygame

pygame.font.init()



def main():
    # Establecer el tamaño de la ventana y lo mete en una variable
    win = pygame.display.set_mode((1600,1000))

    # Establecer el título de la ventana
    pygame.display.set_caption("Ventana de Test1")

    # La pinta de color blanco el fondo
    win.fill((255,255,255))

    # Ejecución de programa
    # Quitar las señales a las partes que quiero ejecutar

    
    

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

