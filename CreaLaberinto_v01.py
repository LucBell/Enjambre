# Creación del entorno

# Carga Librerías

import os
# Lugar donde aparece la ventana
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

import random # Para los números aleatorios
import pygame
import time
import pickle

# Carga los programas comunes
from Comunes_v01 import *

# Inicializa pygame

pygame.font.init()

# Declaraciones variables principales

# Variable Entorno es lista
entorno = []

# Longitud de la lista
# print("Longitud Lista: ",len(entorno))

# Pedir Tamaño del mapa y % de bordes
# tamX = int(input("Tamaño Horizontal 156? "))
# tamY = int(input("Tamaño Vertical 96? "))
# bordes = int(input("Porcentaje de bordes (1-100) 25?"))


def genera_el_entorno():
    # Con esta función creamos los bordes aleatorios y los cargamos en la variable entorno

    global entorno
    
    for coordX in range(0,tamX):
        for coordY in range(0,tamY):
            
            # Bordes aleatorios
            bordAr = random.randint(0,100)
            if bordAr > bordes: bordAr = 0
            else: bordAr = 1
            bordAb = random.randint(0,100)
            if bordAb > bordes: bordAb = 0
            else: bordAb = 1
            bordIz = random.randint(0,100)
            if bordIz > bordes: bordIz = 0
            else: bordIz = 1
            bordDe = random.randint(0,100)
            if bordDe > bordes: bordDe = 0
            else: bordDe = 1

            # Vaciar casillas exteriores (Salvo su borde interior)
            if coordX == 0:
                bordIz = 0
                bordAr = 0
                bordDe = 1
                bordAb = 0
            if coordX == (tamX-1):
                bordIz = 1
                bordAr = 0
                bordDe = 0
                bordAb = 0
            if coordY == 0:
                bordIz = 0
                bordAr = 1
                bordDe = 0
                bordAb = 0
            if coordY == (tamY-1):
                bordIz = 0
                bordAr = 0
                bordDe = 0
                bordAb = 1

            # Fijar bordes exteriores, para que coincidan con anteriores
            # Pruebo a poner una casilla para dentro.
            if coordX == 1:
                bordIz =1
            if coordX == (tamX-2):
                bordDe =1
            if coordY == 1:
                bordAb =1
            if coordY == (tamY-2):
                bordAr =1
            
            entorno += [[coordX,coordY, bordIz, bordAr, bordDe, bordAb]]
        
    print("Longitud Lista: ",len(entorno))

# print(entorno)

def homogeneiza_bordes():
    # Hacer iguales los bordes a los dos lados de la casilla
    # Homogeneiza los bordes horizontales (se asegura que tienen el borde activado las dos celdas colindantes
    # Tengo que revisarlo para que me respete las casillas exteriores

    global entorno

    for casilla in range(0,len(entorno)-1):
        casillaCheck = entorno[casilla]
        ## print("check", casillaCheck[0:2])
        casillaArriba = entorno[casilla +1]
        if casillaCheck[3] == 1 or casillaArriba[5] == 1:
            if not(casillaCheck[3] == 1 and casillaArriba[5] == 1):
                    # print("Antes: Abajo",casilla1[5], "Arriba", casillaAbajo[3])
                    # print("Antes", casilla1, casillaAbajo)
                    ## print("Corregido Arriba:", casillaCheck[0:2])
                    casillaCheck[3] = 1
                    casillaArriba[5] = 1
                    # print("Después: Abajo",casilla1[5], "Arriba", casillaAbajo[3])
                    # print("Después", casilla1, casillaAbajo)

    # Homogeneiza los bordes verticales
                
        if not casilla + tamY > len(entorno)-1:
            casillaDcha = entorno[casilla +tamY]
            if casillaCheck[4] == 1 or casillaDcha[2] == 1:
                if not(casillaCheck[4] == 1 and casillaDcha[2] == 1):
                # print("Antes: Izda",casilla1[4], "Dcha", casilla2[2])
                # print("Antes", casilla1, casilla2)
                    ## print("Corregido Dcha:", casillaCheck[0:2])
                    casillaCheck[4] = 1
                    casillaDcha[2] = 1
                # print("Después: Izda",casilla1[4], "Dcha", casilla2[2])
                # print("Después", casilla1, casilla2)

# print(entorno)


def libera_cuadrados():
    
    # Reviso todas las casillas y abro las que están completamente cerradas
    # Esto lo tengo que revisar por el borde exterior...

    global entorno

    for casilla in range(0,len(entorno)):
        casillaCheck = entorno[casilla]
        sumaBordes = sum(casillaCheck[2:6]) # se suma desde el item 3 (los anteriores son el 0 y el 1, hasta el item (6-1) = 5)
        ## print("Suma casillas: ", casillaCheck, sumaBordes)
        if sumaBordes == 4:
            bordeLibre = random.randint(2,5)
            ## print("Borde Liberado: ", bordeLibre)
            
            # Limpia también casilla anexa al Borde Izquierdo
            if bordeLibre == 2:
                if casillaCheck[0] != 0:
                    casillaAnexa = entorno[casilla-tamY]
                    casillaAnexa[4] = 0
                else:
                    bordeLibre = 3

            # Limpia también casilla anexa al Borde Superior
            if bordeLibre == 3:
                if casillaCheck[1] != tamY-1:
                    casillaAnexa = entorno[casilla+1]
                    casillaAnexa[5] = 0
                else:
                    bordeLibre = 4
                
            # Limpia también casilla anexa al Borde Derecho
            if bordeLibre == 4:
                if casillaCheck[0] != tamX-1:
                    casillaAnexa = entorno[casilla+tamY]
                    casillaAnexa[2] = 0
                else:
                    bordeLibre = 5
              
            # Limpia también casilla anexa al Borde Inferior
            if bordeLibre == 5:
                if casillaCheck[1] != 0:
                    casillaAnexa = entorno[casilla-1]
                    casillaAnexa[3] = 0
                elif casillaCheck[0] == 0: # Esto lo tengo que poner por la casilla 0,0
                    bordeLibre = 3
                    casillaAnexa = entorno[casilla+1]
                    casillaAnexa[5] = 0
                else: # Esto lo tengo que poner por todo el borde de abajo
                    bordeLibre = 2
                    if casillaCheck[0] != 0:
                        casillaAnexa = entorno[casilla-tamY]
                        casillaAnexa[4] = 0

            casillaCheck[bordeLibre] = 0

            ## print("Casilla Anexa: ", casillaAnexa)

            ## print("Casilla liberada: ",casillaCheck)

# --------------------------------------------------------------          

def eliminadorParejasVerticales():
    # Como su nombre indica, sirve para abrir los espacios
    # cerrados de dos celdas en formato vertical
    # solo afecta a las celdas interiores, no a los bordes

    global entorno    
    
    for casX in range(1,tamX-3):
        for casY in range(1,tamY-3):
            casilla = tamY + casX*tamY + casY + 1
            casillaCheck = entorno[casilla]

            # se suma desde el item 3 (los anteriores son el 0 y el 1, hasta el item (6-1) = 5)
            sumaBordes = sum(casillaCheck[2:6]) 
            
            # print("Suma casillas: ", casillaCheck, sumaBordes)
            if sumaBordes == 3:
                bordeLibre = casillaCheck.index(0,2)
                ## print("Candidato!",casillaCheck,bordeLibre)
                if bordeLibre == 2:
                    casillaAnexa = entorno[casilla-tamY]
                elif bordeLibre == 3:
                    casillaAnexa = entorno[casilla+1]
                elif bordeLibre == 4:
                    casillaAnexa = entorno[casilla+tamY]
                elif bordeLibre == 5:
                    casillaAnexa = entorno[casilla-1]
                sumaBordesAnexa = sum(casillaAnexa[2:6])
                if sumaBordesAnexa == 3:
                    borde_A_Liberar = random.randint(2,5)
                    ## print("Borde a liberar Aleat:", borde_A_Liberar)

                    # Si me sale en el aleatorio el borde que ya estaba libre lo cambio por el siguiente

                    if borde_A_Liberar == bordeLibre:
                        if borde_A_Liberar ==5:
                            borde_A_Liberar = 2
                        else:
                            borde_A_Liberar += 1
                            
                    ## print("Borde a liberar Final:", borde_A_Liberar)
                    casillaCheck[borde_A_Liberar] = 0
                    ## print("Liberada! ", casillaCheck)
                    unificaBordesConAdyacentesCasilla(borde_A_Liberar,casillaCheck,casilla)
                    

# --------------------------------------------------------------

def unificaBordesConAdyacentesCasilla(bordeLibre, casillaCheck,casilla):
    #Este programa sirve para unificar los bordes modificados con las adyacentes.
    # Lo tengo que revisar para ajustar los bordes nuevos...

    global entorno

    ## print("Adyacentes, bordeLibre: ", bordeLibre, " casillaCheck: ",casillaCheck, " Casilla: ", casilla)
    ## casilla = entorno.index(casillaCheck)
    ## print("Nueva casilla: ", casilla)

    # Limpia también casilla anexa al Borde Izquierdo
    if bordeLibre == 2:
        if casillaCheck[0] != 0:
            casillaAnexa = entorno[casilla-tamY]
            casillaAnexa[4] = 0

    # Limpia también casilla anexa al Borde Superior
    if bordeLibre == 3:
        if casillaCheck[1] != tamY-1:
            casillaAnexa = entorno[casilla+1]
            casillaAnexa[5] = 0
                
    # Limpia también casilla anexa al Borde Derecho
    if bordeLibre == 4:
        if casillaCheck[0] != tamX-1:
            casillaAnexa = entorno[casilla+tamY]
            casillaAnexa[2] = 0
              
    # Limpia también casilla anexa al Borde Inferior
    if bordeLibre == 5:
        if casillaCheck[1] != 0:
            casillaAnexa = entorno[casilla-1]
            casillaAnexa[3] = 0

    ## print("Unificada! ", casillaAnexa)

# --------------------------------------------------------------

def guardar_hormiguero():
    # Función para guardar el entorno en un fichero
    # Prueba de almacenamiento como binario de forma global
    #   utilizando el programa pickle

    global entorno

    with open("Datos/DatosEntorno"+str(tamX)+"x"+str(tamY)+".txt", 'wb') as fp:
        pickle.dump(entorno, fp)
        print('Done writing list into a binary file')
   
def genera_entorno_aleatorio():
    # Programa gestor de las subrutinas de la creación aleatoria
    # Esto me lo debería llevar a otro fichero para aligerar este
    genera_el_entorno()
    homogeneiza_bordes()
    # libera_cuadrados() # No lo puedo activar hasta que arregle con el nuevo borde
    # eliminadorParejasVerticales() # No lo puedo activar hasta que arregle con el nuevo borde.

    # Cuando genero un hormiguero, lo guardo por si quiero repetir
    guardar_hormiguero()
    print("Hormiguero guardado.")

def inicio(win):
    # Programa que inicia los pasos de generación del laberinto

    global entorno
    entorno = []

    # Borro el hormiguero pintando encima
    com_borrar_hormiguero(win,dispX,dispY,bordX,bordY)

    # genero el hormiguero
    genera_entorno_aleatorio()

    # Pinto el hormiguero
    com_pintar_hormiguero(bordX,bordY,win,entorno,dispX,dispY,tamX,tamY,tc)

    # Esto es necesario para que se vea lo que pinto
    pygame.display.update()


def main():
    # Este es el programa principal de Ejecución
    # Tiene algunos trozos de programa, que se podrían delegar fuera, para dejar solo lo principal
    
    # Establecer el tamaño de la ventana y lo mete en una variable
    win = pygame.display.set_mode((dispX,dispY))

    # Establecer el título de la ventana
    pygame.display.set_caption("Swarm AI")

    # Ejecución de programa
    # Quitar las señales a las partes que quiero ejecutar

    # Pongo los textos
    com_text_on_screen(win,tamX,tamY)

    # Programa principal
    inicio(win)

    # Ejemplo de como mantener un programa corriendo hasta que cambias una variable.
    # Paso 1. Defines la variable
    run = True
    # Paso 2. Mientras no la cambies a False, sigue corriendo en loop
    while run:
        # Esto es necesario para que puedas cerrar la ventana creada pulsando en la X de arriba
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                if 20 <= x_mouse <= 120 and 160 <= y_mouse <= 185:
                    # este lo guardo para otros botones
                    inicio(win)
                elif 20 <= x_mouse <= 120 and 120 <= y_mouse <= 145:
                    run = False
        # si actualizo datos, puedos pintarlos en este loop
        # pintarR02(50,50,win)
        # Esto es fundamental para que se vea bien lo que pinto.
        # pero no parece que haga falta que esté en el while... salvo que pinte cosas
        # nuevas, aun pintando paredes nuevas, no parece hacer falta aquí.
        # pygame.display.update()




# Ejecuto el programa principal y salgo cuando se termina el mismo.
main()
pygame.quit()

# --------------------------------------------------------------

# Programas auxiliares

def modificar_laberinto():
    # Programa para modificar el laberinto, porque al tener el fichero
    #   en binario ya no puedo manualmente

    global entorno

    # Primero cargo el laberinto
    obtener_entorno_de_fichero()

    # Digo las celdas que quiero cambiar
    casilla_ppal = entorno[93]
    casilla_opuesta = entorno[94]
    print("Casillas Antes: ", casilla_ppal, casilla_opuesta)
    casilla_ppal[2+1] = 0
    casilla_opuesta[4+1] = 0
    print("Casillas Después: ", casilla_ppal, casilla_opuesta)

    # Grabo de nuevo el laberinto
    guardar_hormiguero()



# modificar_laberinto()
# pygame.quit()