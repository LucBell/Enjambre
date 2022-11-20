# Creación del entorno

# Carga Librerías

import os
# Lugar donde aparece la ventana
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

import random # Para los números aleatorios
import pygame
import time
import turtle


# Inicializa pygame

pygame.font.init()

# Declaraciones variables principales

# Variable Entorno es una lista

entorno = []
# print(type(entorno))

# Tamaño Display

dispX = 1900
dispY = 1010



# Tamaño Bordes

bordX = 300
bordY = 20

# Longitud de la lista

# print("Longitud Lista: ",len(entorno))

# Pedir Tamaño del mapa y % de bordes

# tamX = int(input("Tamaño Horizontal 156? "))
# tamY = int(input("Tamaño Vertical 96? "))
# bordes = int(input("Porcentaje de bordes (1-100) 25?"))

tamX = 10
tamY = 10
bordes = 20

##print(tamX)
##print(tamY)
##print(type(tamX))

# Carga de la lista

def carga_del_entorno():
    
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

            # Fijar bordes exteriores
            if coordX == 0:
                bordIz =1
            if coordX == (tamX-1):
                bordDe =1
            if coordY == 0:
                bordAb =1
            if coordY == (tamY-1):
                bordAr =1
            
            # Creación de las características de la casilla
            # Tengo que cambiar el nombre de los bordes, porque al pasar
            # a Gitpod han cambiado. Ahora tenemos:
            # 1. bordIz (este no ha cambiado)
            # 2. bordAb (Cambio!)
            # 3. bordDe (este no ha cambiado)
            # 4. bordAr (Cambio!)
            entorno += [[coordX,coordY, bordIz, bordAr, bordDe, bordAb]]
        
    print("Longitud Lista: ",len(entorno))

# print(entorno)

def homogeneiza_bordes():
    
    # Hacer iguales los bordes a los dos lados de la casilla
    
    # Homogeneiza los bordes horizontales (se asegura que tienen el borde activado las dos celdas colindantes

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
    for casX in range(0,tamX-2):
        for casY in range(0,tamY-2):
            casilla = tamY + casX*tamY + casY + 1
            casillaCheck = entorno[casilla]
            sumaBordes = sum(casillaCheck[2:6]) # se suma desde el item 3 (los anteriores son el 0 y el 1, hasta el item (6-1) = 5)
            ## print("Suma casillas: ", casillaCheck, sumaBordes)
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

    # Limpia también casilla anexa al Borde Izquierdo
    ## print("Adyacentes, bordeLibre: ", bordeLibre, " casillaCheck: ",casillaCheck, " Casilla: ", casilla)

    ## casilla = entorno.index(casillaCheck)
    ## print("Nueva casilla: ", casilla)
    
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


def pintarR02(origenX,origenY,win):
    
# Utilizando pygame defino una función para pintar el entorno
# Esto lo hice complicado porque estaba en turtle e iba muy lento
# En pygame va rápido por lo que lo puedo simplificar

# Primero pinto los bordes
   
    for casilla in range(0, tamY):
        casillaCheck = entorno[casilla]
        pintarR02a(origenX,origenY,casillaCheck,win)

        casillaCheck = entorno[casilla+tamY*(tamX-1)]
        pintarR02a(origenX,origenY,casillaCheck,win)

    for casilla in range(0, tamX-1):
        casillaCheck = entorno[tamY+casilla*tamY]
        pintarR02a(origenX,origenY,casillaCheck,win)

        casillaCheck = entorno[tamY*2-1+casilla*tamY]
        pintarR02a(origenX,origenY,casillaCheck,win)

# Luego el interior alternando celdas

    for columna in range(0, tamX-2):
        for fila in range(0,tamY//2):
            if columna%2==0:
                tieneQueSerImpar =1
            else:
                tieneQueSerImpar= 0
                
            casillaCheck = entorno[tamY+1+columna*tamY+fila*2+tieneQueSerImpar]
            ## print(columna, fila,casillaCheck,tieneQueSerImpar)

            pintarR02a(origenX,origenY,casillaCheck,win)

def pintarR02a(origenX,origenY,casillaCheck,win):

    # Defino el tamaño de las casillas y el origen de cada una
    # 10 para tamaño pequeño

    tcX = (dispX-40)/tamX
    tcY = (dispY-40)/tamY
    tc = min (tcX, tcY)

    posX = casillaCheck[0]*tc+origenX
    posY = casillaCheck[1]*tc+origenY

    # Pintar lados Casilla
    
    if casillaCheck[2]==1:
        pygame.draw.line(win, (0, 0, 0), (posX, posY), (posX, posY+tc), 3)

    if casillaCheck[3]==1:
        pygame.draw.line(win, (0, 0, 0), (posX, posY+tc), (posX+tc, posY+tc), 3)

    if casillaCheck[4]==1:
        pygame.draw.line(win, (0, 0, 0), (posX+tc, posY+tc), (posX+tc, posY), 3)

    if casillaCheck[5]==1:
        pygame.draw.line(win, (0, 0, 0), (posX+tc, posY), (posX, posY), 3)

def hormiguero(win):
    # Selecciono origen hormiguero aleatorio
    horm = random.randint(0,len(entorno)-1)
    print ("Hormiguero en: ",horm)
    print (entorno[horm])
    casilla_horm = entorno[horm]
    ch_X = casilla_horm[0]
    ch_Y = casilla_horm[1]

    # El tamaño del cuadrado lo debería hacer con una variable global o no local.

    tcX = (dispX-40)/tamX
    tcY = (dispY-40)/tamY
    tc = min (tcX, tcY)

    pygame.draw.rect(win, (201, 135, 58), (ch_X*tc+bordX,ch_Y*tc+bordY, tc, tc), 0)

    print ("Coord horm",ch_X, ch_Y, ch_X*tc, ch_Y*tc )

    return horm

def comida(win):

    # Selecciono destino comida aleatorio
    # Pendientes: Si sale el mismo sitio que el hormiguero, tendría que buscar otro sitio.
    
    comi = random.randint(0,len(entorno)-1)

    # print ("Comida en: ",comi)
    # print (entorno[comi])

    # Saco coordenadas de la casilla seleccionada

    casilla_comi = entorno[comi]
    cc_X = casilla_comi[0]
    cc_Y = casilla_comi[1]

    # El tamaño del cuadrado lo debería hacer con una variable global o no local.

    tcX = (dispX-40)/tamX
    tcY = (dispY-40)/tamY
    tc = min (tcX, tcY)

    # Dibujo rectágulo en la casilla seleccionada

    pygame.draw.rect(win, (41, 158, 41), (cc_X*tc+bordX,cc_Y*tc+bordY, tc, tc), 0)

    # print ("Coord comi",cc_X, cc_Y, cc_X*tc, cc_Y*tc )

    return comi


def paseo_hormiga1(horm,comi):
    # Hormiga que pasea por el hormiguero y que cuando encuentra la comida,
    # vuelve marcando las casillas como "comida encontrada"
    # también tiene que levantar muros si se encuentra casillas bloqueadas

    # defino variable con el histórico del paseo
    recorrido_hormiga = []

    # Coloco la hormiga en el hormiguero

    pos_horm = (horm)
    casilla = entorno[pos_horm]

    recorrido_hormiga.append(pos_horm)

    print("Posición inicial: ",horm, casilla)
    print("Objetivo: ",comi, entorno[comi])

    # recorrido_hormiga += pos_horm

    # Creo un loop hasta que encuentre la comida

    aguante_hormiga = 500

    for stamina in range(1,aguante_hormiga+1):
        # Decido hacia donde me muevo
        # Aquí habrá que poner probabilidades según las indicaciones
        # de las casillas adyacentes
        # print ("Intento número: ", stamina)
        dir_objetivo = random.randint(1, 4)
        # print ("Dirección: ", dir_objetivo)
        # Compruebo si hay barrera

        casilla = entorno[pos_horm]

        if casilla[dir_objetivo+1] == 0:
            direcciones = [-tamY,1,tamY,-1]
            # print("Sumar para mover?: ", direcciones[dir_objetivo-1])
            pos_horm += direcciones[dir_objetivo-1]
            # recorrido_hormiga += pos_horm
            casilla = entorno[pos_horm]
            # print ("Me muevo a: ", pos_horm, casilla)
            # print ("He recorrido: ", recorrido_hormiga)
            
            # Aquí voy a añadir la casilla al recorrido
            # o si he hecho un bucle, lo voy a borrar
            if pos_horm in recorrido_hormiga:
                inicio_borrado = recorrido_hormiga.index(pos_horm)
                fin_borrado = len(recorrido_hormiga)
                del recorrido_hormiga[inicio_borrado+1:fin_borrado]
            
            # Si no ha encontrado el mismo, lo añado al recorrido
            else:
                recorrido_hormiga.append(pos_horm)
            
            print ("He recorrido: ", recorrido_hormiga)

        else:
            # print("No me muevo y lo intento de nuevo")
            pass

        if pos_horm== comi:
            print("Encontré la comida!! En el intento: ", stamina)
            print("He necesitado los siguientes pasos: ", len(recorrido_hormiga))
            print(recorrido_hormiga)
            break

        # print("Posición",casilla)

        # cas_objetivo

        # casilla_objetivo = entorno[dir]

        # Luego compruebo si estoy en la comida para pararlo


def text_on_screen(win):
    font = pygame.font.SysFont(None, 24)
    img = font.render("Swarm", True, 1)
    win.blit(img, (20, 20))





def main():
    # Establecer el tamaño de la ventana y lo mete en una variable
    win = pygame.display.set_mode((dispX,dispY))

    # Establecer el título de la ventana
    pygame.display.set_caption("Swarm AI")

    # La pinta de color blanco el fondo
    win.fill((255,255,255))

    # Ejecución de programa
    # Quitar las señales a las partes que quiero ejecutar

    text_on_screen(win)

    carga_del_entorno()

    homogeneiza_bordes()

    print("Ahora vamos a liberar cuadrados...")

    libera_cuadrados()

    print("Ahora probamos a eliminar las parejas cerradas interiores...")

    eliminadorParejasVerticales()

    horm = hormiguero(win)
    comi = comida(win)

    print("Terminé!")

    # Ejemplo de como mantener un programa corriendo hasta que cambias una variable.

    # Defines la variable
    run = True

    pintarR02(bordX,bordY,win)

    # Saco a pasear a la hormiga

    paseo_hormiga1(horm,comi)

    # Mientras no la cambies a False, sigue corriendo en loop
    while run:

        # Esto es necesario para que puedas cerrar la ventana creada pulsando en la X de arriba
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # si actualizo datos, puedos pintarlos en este loop
        # pintarR02(50,50,win)
        pygame.display.update()





main()
pygame.quit()

# --------------------------------------------------------------

