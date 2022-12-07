# Creación del entorno

# Carga Librerías

import os
# Lugar donde aparece la ventana
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

import random # Para los números aleatorios
import pygame
import time
import turtle

# from pygame.locals import *

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

tamX = 5
tamY = 5
bordes = 25

##print(tamX)
##print(tamY)
##print(type(tamX))

# Carga de la lista

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

    global entorno

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

    # Para que los cuadrados no tapen los bordes, les quito un 10% de área.

    bordeblanco = tc/10

    pygame.draw.rect(win, (201, 135, 58), (ch_X*tc+bordX+bordeblanco,ch_Y*tc+bordY+bordeblanco, tc-bordeblanco*2, tc-bordeblanco*2), 0)

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

    # Para que los cuadrados no tapen los bordes, les quito un 10% de área.

    bordeblanco = tc/10

    # Dibujo rectágulo en la casilla seleccionada

    pygame.draw.rect(win, (41, 158, 41), (cc_X*tc+bordX+bordeblanco,cc_Y*tc+bordY+bordeblanco, tc-bordeblanco*2, tc-bordeblanco*2), 0)

    # print ("Coord comi",cc_X, cc_Y, cc_X*tc, cc_Y*tc )

    return comi


def paseo_hormiga1(win,horm,comi):
    # Hormiga que pasea por el hormiguero y que cuando encuentra la comida,
    # vuelve marcando las casillas como "comida encontrada"
    # también tiene que levantar muros si se encuentra casillas bloqueadas

    global entorno

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

            pintar_camino(win, recorrido_hormiga)

            break

        # print("Posición",casilla)

        # cas_objetivo

        # casilla_objetivo = entorno[dir]

        # Luego compruebo si estoy en la comida para pararlo

def pintar_camino(win, recorrido_hormiga):
    # Con esta función quiero pintar el recorrido que ha seguido la hormiga.

    # Creo que lo podría simplificar simplemente recorriendo la variable
    # recorrido_hormiga con la función for
    for celda_a_pintar in range (1,len(recorrido_hormiga)-1):
        
        paso_hormiga = recorrido_hormiga[celda_a_pintar]
        casilla_pintar = entorno[paso_hormiga]

        # print(casilla_pintar)

        # Saco coordenadas de la casilla seleccionada
        cp_X = casilla_pintar[0]
        cp_Y = casilla_pintar[1]
        
        # El tamaño del cuadrado lo debería hacer con una variable global o no local.

        tcX = (dispX-40)/tamX
        tcY = (dispY-40)/tamY
        tc = min (tcX, tcY)

        # Para que los cuadrados no tapen los bordes, les quito un 10% de área.
        bordeblanco = tc/10        
    
        # Dibujo rectágulo en la casilla seleccionada

        pygame.draw.rect(win, (236, 250, 230), (cp_X*tc+bordX+bordeblanco,cp_Y*tc+bordY+bordeblanco, tc-bordeblanco*2, tc-bordeblanco*2), 0)
        



def text_on_screen(win):

    

    # Defino las fuentes
    fontA = pygame.font.SysFont(None, 50)
    fontB = pygame.font.SysFont(None, 30)

    # Texto Título
    text1 = fontA.render("Swarm", True, 0)
    win.blit(text1, (20, 20))
    
    # Textos de datos
    # Título Tamaño
    text2 = fontB.render("Tamaño: ", True, 0)
    win.blit(text2, (20, 80))

    # Campo para el tamaño
    # Texto inicial
    text3 = str(tamX)+"x"+str(tamY)
    img3 = fontB.render(text3, True, 0)
    win.blit(img3, (120, 80))



    # Esto se supone que es para poder poner los datos, pero no funciona.

    # Rectángulo para tomar los datos
    # rect3 = img3.get_rect()
    # rect3.topleft = (120, 80)
    # cursor3 = Rect(rect3.topright, (3, rect3.height))

    # running = True

    # while running:
    #     for event in pygame.event.get():
    #         if event.type == KEYDOWN:
    #             if event.key == K_BACKSPACE:
    #                 if len(text3)>0:
    #                     text3 = text3[:-1]
    #             else:
    #                 text3 += event.unicode
    #             img3 = fontB.render(text3, True, 0)
    #             rect3.size=img3.get_size()
    #             cursor3.topleft = rect3.topright
    
    #     win.blit(img3, rect3)
    #     if time.time() % 1 > 0.5:
    #         pygame.draw.rect(win, 0, cursor3)
    #     pygame.display.update()

def guardar_hormiguero():
    # Función para guardar el entorno en un fichero

    global entorno

    with open("Datos/DatosEntorno.txt",'w',encoding = 'utf-8') as f:
        for casillas in entorno:
            for datos in casillas:
                f.write(str(datos))
            # f.write("-")

def obtener_entorno_de_fichero():
    # Función para cargar el entorno de un fichero en vez de generarlo cada vez.

    global entorno

    with open("Datos/DatosEntorno.txt",'r',encoding = 'utf-8') as f:
        # Saco el tamaño del entorno
        file_stat= os.stat("Datos/DatosEntorno.txt")
        file_size = file_stat.st_size

        # Calculo cuantas casillas tiene el fichero

        numero_casillas = int(file_size/6)

        #print("Número de casillas= ", numero_casillas)

        # Saco los datos de cada casilla y lo meto en el entorno

        for casilla in range(numero_casillas):
            # Defino una lista para cada casilla
            def_casilla = []

            # Relleno la lista de la casilla con sus datos
            for coord in range (6):
                # print("Coord: ",coord)
                dato = f.read(1)
                #print("Dato: ",dato)
                dato_num = int(dato)
                def_casilla += [dato_num]
            #print("Def_casilla: ",def_casilla)
            
            # Meto toda la casilla en la variable entorno
            entorno += [def_casilla]
            
            # Borro los datos de la variable
            del def_casilla
        # print(entorno)

def carga_entorno():
    # Esto sirve para generar el hormiguero o cargar el que tenemos guardado
    
    respuesta = input("Genero nuevo el entorno (s/n): ") 
    if respuesta == "s":
        genera_el_entorno()
        homogeneiza_bordes()
        libera_cuadrados()
        eliminadorParejasVerticales()
         
    elif respuesta == "n":
        obtener_entorno_de_fichero()
         
    else: 
        print("Por favor solo respuestas s/n...")
        pygame.quit()


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

    # Desactivo la carga para que siempre se cargue de fichero
    # Activar siguiente línea y desactivar la siguiente para que vuelva a preguntar
    # si queremos generar uno nuevo.

    #carga_entorno()
    obtener_entorno_de_fichero()

    # Defino dónde está el hormiguero y dónde la comida
    # Esto lo tengo que meter en un fichero para poder guardarlo
    
    horm = hormiguero(win)
    comi = comida(win)

    print("Terminé!")

    # Ejemplo de como mantener un programa corriendo hasta que cambias una variable.

    # Defines la variable
    run = True

    pintarR02(bordX,bordY,win)

    # Saco a pasear a la hormiga

    paseo_hormiga1(win,horm,comi)

    pygame.display.update()

    # Antes de salir guardo en un fichero mi hormiguero

    # print("Este es el entorno que estás utilizando: ",entorno)
    guardar_hormiguero()
    # print("Hormiguero guardado.")

    # Mientras no la cambies a False, sigue corriendo en loop
    while run:

        # Esto es necesario para que puedas cerrar la ventana creada pulsando en la X de arriba
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # si actualizo datos, puedos pintarlos en este loop
        # pintarR02(50,50,win)
        
        # Esto es fundamental para que se vea bien lo que pinto.
        # pero no parece que haga falta que esté en el while... salvo que pinte cosas
        # nuevas
        # pygame.display.update()





main()



pygame.quit()

# --------------------------------------------------------------

