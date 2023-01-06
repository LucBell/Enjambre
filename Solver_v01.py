# Creación del entorno

# Carga Librerías

import os
# Lugar donde aparece la ventana
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

import random # Para los números aleatorios
import pygame
import time
import pickle

# Carga los otros programas
from Comunes_v01 import *

# Inicializa pygame

pygame.font.init()

# Declaraciones variables principales

# Variable Entorno y feromona son listas

entorno = []
feromona = []

# Defino las variables para medir el éxito de la estrategia
# Track_sucess es una lista con formato: Éxitos, fracasos, total, % éxitos, % fracasos, número de pasos recorrido más corto, recorrido más corto

exitos = 0
fracasos = 0
total_intentos = 0
exitos_porc = 0
fracasos_porc = 0
recorrido_corto_num = 0
recorrido_corto = []
track_success = [exitos,fracasos,total_intentos,exitos_porc,fracasos_porc,recorrido_corto_num,recorrido_corto]

# Tamaño Display
dispX = 1900
dispY = 1010

# Tamaño Bordes. Esto define el borde superior y el izquierdo
# para ver dónde pinta el hormiguero
bordX = 200
bordY = 20

# Fijo el Tamaño para test de las variables principales
tamX = 20
tamY = 10
bordes = 25
feromona_inicial = 10

# Almaceno en una lista cómo varía el indicador de posición según
# en qué dirección se mueva la hormiga
direcciones = [-tamY,1,tamY,-1]

def carga_inicial_feromona():
    # Programa que carga con ceros la lista feromona al inicio
    
    global feromona, feromona_inicial

    for coordX in range(0,tamX):
        for coordY in range(0,tamY):
            feromona +=[feromona_inicial]
    # print("Feromona inicial: ", feromona)

def pintar_hormiguero(origenX,origenY,win):
    
# Utilizando pygame defino una función para pintar el entorno
# Esto lo hice complicado porque estaba en turtle e iba muy lento
# En pygame va rápido por lo que lo puedo simplificar

# Primero pinto los bordes
   
    for casilla in range(0, tamY):
        casillaCheck = entorno[casilla]
        pintar_bordes_casilla(origenX,origenY,casillaCheck,win)

        casillaCheck = entorno[casilla+tamY*(tamX-1)]
        pintar_bordes_casilla(origenX,origenY,casillaCheck,win)

    for casilla in range(0, tamX-1):
        casillaCheck = entorno[tamY+casilla*tamY]
        pintar_bordes_casilla(origenX,origenY,casillaCheck,win)

        casillaCheck = entorno[tamY*2-1+casilla*tamY]
        pintar_bordes_casilla(origenX,origenY,casillaCheck,win)

# Luego el interior alternando celdas

    for columna in range(0, tamX-2):
        for fila in range(0,tamY//2):
            if columna%2==0:
                tieneQueSerImpar =1
            else:
                tieneQueSerImpar= 0
                
            casillaCheck = entorno[tamY+1+columna*tamY+fila*2+tieneQueSerImpar]
            ## print(columna, fila,casillaCheck,tieneQueSerImpar)

            pintar_bordes_casilla(origenX,origenY,casillaCheck,win)

def pintar_bordes_casilla(origenX,origenY,casillaCheck,win):
    # Programa para pintar los bordes de una casilla determinada
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


def pinto_cuadro (win, color, casilla):

    # Programa para pintar cuadros en el hormiguero

    casilla_pintar = entorno[casilla]
    coord_X = casilla_pintar[0]
    coord_Y = casilla_pintar[1]

    # El tamaño del cuadrado lo debería hacer con una variable global o no local.

    tcX = (dispX-40)/tamX
    tcY = (dispY-40)/tamY
    tc = min (tcX, tcY)

    # Para que los cuadrados no tapen los bordes, les quito un 10% de área.

    bordeblanco = tc/10

    # Dibujo el cuadrado

    pygame.draw.rect(win, color, (coord_X*tc+bordX+bordeblanco,coord_Y*tc+bordY+bordeblanco, tc-bordeblanco*2, tc-bordeblanco*2), 0)


def hormiguero(win):
    # Programa para situar el hormiguero

    global horm

    # Selecciono origen hormiguero aleatorio (tengo que cambiar por el tema de los bordes)
    # horm = random.randint(0,len(entorno)-1)

    # Fijo el hormiguero en un punto fijo
    horm = 2*tamY+tamY//2

    print ("Hormiguero en: ",horm)
    print (entorno[horm])
    
    color_hormiguero = (201, 135, 58)

    pinto_cuadro(win, color_hormiguero, horm)

    return horm

def comida(win):
    # Programa para situar la comida

    global comi

    # Selecciono origen hormiguero aleatorio (tengo que cambiar por el tema de los bordes)
    # comi = random.randint(0,len(entorno)-1)

    # Fijo el hormiguero en un punto fijo
    comi = len(entorno)-1-(2*tamY+tamY//2)

    # print ("Comida en: ",comi)
    # print (entorno[comi])
    
    color_comida = (91, 155, 213)

    pinto_cuadro(win, color_comida, comi)

    return comi



def paseo_hormiga1(win,horm,comi):
    # Hormiga que pasea por el hormiguero y que cuando encuentra la comida,
    # vuelve marcando las casillas como "comida encontrada"
    # también tiene que levantar muros si se encuentra casillas bloqueadas

    # Carga variables globales
    global entorno
    global exitos, fracasos, recorrido_corto

    # defino variable con el histórico del paseo
    recorrido_hormiga = []

    # Coloco la hormiga en el hormiguero
    pos_horm = (horm)
    casilla = entorno[pos_horm]
    recorrido_hormiga.append(pos_horm)

    # Textos para ayudarme a analizar el código
    # print("Posición inicial: ",horm, casilla)
    # print("Objetivo: ",comi, entorno[comi])

    # recorrido_hormiga += pos_horm

    # Creo un loop hasta que encuentre la comida
    aguante_hormiga = (tamX+tamY)*6

    for stamina in range(1,aguante_hormiga+1):
        # Decido hacia donde me muevo
        # Aquí habrá que poner probabilidades según las indicaciones
        # de las casillas adyacentes
        # print ("Intento número: ", stamina)
        dir_objetivo = random.randint(1, 4)
        # print ("Dirección: ", dir_objetivo)
        # Compruebo si hay barrera

        casilla = entorno[pos_horm]
        
        # Calculo la probabilidad que tiene cada lado de ser el destino de la hormiga
        # Primero cargo la variable muro con cero si hay muro (lo contrario que he
        # hecho en la variable entorno...)        
        if casilla[1+1] == 0: muro_1 = 1
        else: muro_1 = 0
        if casilla[2+1] == 0: muro_2 = 1
        else: muro_2 = 0
        if casilla[3+1] == 0: muro_3 = 1
        else: muro_3 = 0
        if casilla[4+1] == 0: muro_4 = 1
        else: muro_4 = 0
        # Aquí calculo la probabilidad de cada dirección.
        #   como multiplico la feromona por el muro. Si hay muro la probabilidad es 0
        prob_de_1 = feromona[pos_horm+direcciones[1-1]]*muro_1
        prob_de_2 = feromona[pos_horm+direcciones[2-1]]*muro_2
        prob_de_3 = feromona[pos_horm+direcciones[3-1]]*muro_3
        prob_de_4 = feromona[pos_horm+direcciones[4-1]]*muro_4
        # Calculo el número total de probabilidad y calculo un número en el rango
        prob_total = prob_de_1+prob_de_2+prob_de_3+prob_de_4
        dir_random = random.randint(0, prob_total)
        # Calculo los rangos para ver a quién le ha tocado
        prob_acu_2 = prob_de_1+prob_de_2
        prob_acu_3 = prob_acu_2+prob_de_3
        # pregunto a ver en qué intervalo ha caído
        if dir_random < prob_de_1: dir_objetivo = 1
        elif dir_random < prob_acu_2: dir_objetivo = 2
        elif dir_random < prob_acu_3: dir_objetivo = 3
        else: dir_objetivo = 4

        # print("Casilla: ",casilla," Probabilidades: ",prob_de_1,prob_acu_2,prob_acu_3,prob_total)
        # print("Dir random: ", dir_random)
        # print("Dir Objetivo: ", dir_objetivo)


        if casilla[dir_objetivo+1] == 0:

            # Compruebo si es un callejón y tomo medidas
            mueve = comprueba_callejon(win, horm, casilla, pos_horm, dir_objetivo)
            # Pongo este cuando quiero probar sin localizador de callejones
            # mueve = True

            # Muevo si no ha habido problemas
            if mueve == True:
                pos_horm += direcciones[dir_objetivo-1]
            else:
                pass

            casilla = entorno[pos_horm]
            #print ("Me muevo a: ", pos_horm, casilla)
            #print ("He recorrido: ", recorrido_hormiga)
            
            # Aquí voy a añadir la casilla al recorrido
            # o si he hecho un bucle, lo voy a borrar
            if pos_horm in recorrido_hormiga:
                inicio_borrado = recorrido_hormiga.index(pos_horm)
                fin_borrado = len(recorrido_hormiga)
                del recorrido_hormiga[inicio_borrado+1:fin_borrado]
            
            # Si no ha encontrado el mismo, lo añado al recorrido
            else:
                recorrido_hormiga.append(pos_horm)
            
            # print ("He recorrido: ", recorrido_hormiga)

        else:
            # print("No me muevo y lo intento de nuevo")
            pass
        
        # Si la posición de la hormiga coincide con la posición de la comida
        #   considero que ha encontrado la comida.
        # La hormiga vuelve al hormiguero depositando la feromona.
        if pos_horm== comi:
            print("Encontré la comida!! En el intento: ", stamina)
            print("He necesitado los siguientes pasos: ", len(recorrido_hormiga))
            print("He recorrido: ",recorrido_hormiga)

            dejar_feromona(recorrido_hormiga)
            pintar_camino(win, recorrido_hormiga)

            # Actualizo el intento como éxito
            exitos+= 1

            # Compruebo si el recorrido es el más corto y lo grabo en la variable
            if len(recorrido_corto) == 0 or len(recorrido_hormiga)<len(recorrido_corto):
                recorrido_corto=recorrido_hormiga

            break

        # Luego compruebo si estoy en la comida para pararlo
        
        # Si llego al final del loop sin haber encontrado nada pongo un mensaje
        if stamina == aguante_hormiga:
            # print ("Intento ",stamina," y no encontré la comida...")

            # Actualizo el intento como fracaso
            fracasos+= 1

            break
        # Compruebo si he entrado en una plaza y levanto muro
        # desactivar para probar sin esta mejora
        comprueba_plaza(win,casilla,pos_horm,dir_objetivo)


def comprueba_plaza(win,casilla,pos_horm,dir_objetivo):
    # Programa para comprobar si hemos entrado en una plaza
    #   En caso afirmativo, levanta una pared para deshacer la plaza

    global entorno

    # print("Casilla: ", casilla, " Dir Objetivo: ", dir_objetivo)

    # Meto la función try para evitar errores con comprobaciones fuera del entorno
    try:
        lista_datos =[(1,1,2,4,2,3,1,4,4,3,1,2),(2,2,3,1,4,3,2,1,4,1,2,3),(3,3,4,2,4,1,3,2,1,2,4,3),(4,4,1,3,1,2,4,3,2,3,1,4)]
        for n in range(4):
            dat = lista_datos[n]
            # print("n: ",n)
            bordes_plaza_dcha = 1
            bordes_plaza_izda = 1
            if dir_objetivo == dat[0]:
                # print(dat)
                celda_anexa_delante = entorno[pos_horm+direcciones[dat[1]-1]]
                celda_anexa_lado_izdo = entorno[pos_horm+direcciones[dat[2]-1]]
                celda_anexa_lado_dcho = entorno[pos_horm+direcciones[dat[3]-1]]
                bordes_plaza_izda = celda_anexa_delante[dat[4]+1]+celda_anexa_delante[dat[5]+1]+celda_anexa_lado_izdo[dat[6]+1]+celda_anexa_lado_izdo[dat[7]+1]
                bordes_plaza_dcha = celda_anexa_delante[dat[8]+1]+celda_anexa_delante[dat[9]+1]+celda_anexa_lado_dcho[dat[10]+1]+celda_anexa_lado_dcho[dat[11]+1]

            if bordes_plaza_izda ==0 or bordes_plaza_dcha ==0:
                # Si detecto plaza, levanto un muro delante (como si hubiese un callejón delante)
                print("Plaza detectada!!")
                pos_horm_futura = pos_horm + direcciones[dir_objetivo-1]
                casilla_futura = entorno[pos_horm_futura]
                levantar_muro_delante(win, casilla, casilla_futura,dir_objetivo)
    except (IndexError):
    # except (RuntimeError, TypeError, NameError, IndexError):
        # print("Detectado")
        pass


def comprueba_callejon(win, horm, casilla, pos_horm,dir_objetivo):
    # Programa para comprobar si la hormiga se ha metido en un callejón
    # Devuelve clave de movimiento o no
    # Levanta muro para cerrar el callejón para el futuro

    global entorno

    # Compruebo si la nueva casilla es un callejón sin salida
    # Lo hago sumando el número de paredes
    pos_horm_futura = pos_horm + direcciones[dir_objetivo-1]
    casilla_futura = entorno[pos_horm_futura]
    barreras_casilla_futura = casilla_futura[2]+casilla_futura[3]+casilla_futura[4]+casilla_futura[5]
    
    if barreras_casilla_futura==3 and pos_horm_futura!=horm:
        
        mueve = False
        print("Callejón!")
        # print("Casilla actual: ", casilla)
        # print("Casilla futura: ", casilla_futura)

        levantar_muro_delante(win, casilla, casilla_futura,dir_objetivo)

    # Si no es un callejón
    # cambio la posición de la hormiga
    else:
        mueve = True
        # pos_horm += direcciones[dir_objetivo-1]
    return mueve

def levantar_muro_delante(win, casilla, casilla_futura,dir_objetivo):
    # Programa para levantar muros en la casilla y en la opuesta
    # Levanto un muro en la casilla
    print("Antes de levantar muro: ",casilla)
    casilla[dir_objetivo+1] = 1
    print("Después de levantar muro: ",casilla)

    # Pinto el muro nuevo en la casilla
    pintar_bordes_casilla(bordX,bordY,casilla,win)
    
    # Calculo la dirección opuesta
    if dir_objetivo > 2:
        dir_opuesta = dir_objetivo-2
    else:
        dir_opuesta = dir_objetivo+2
    
    #Levanto un muro en la casilla opuesta
    casilla_futura[dir_opuesta+1] = 1
    print("Casilla Opuesta modificada: ", casilla_futura)


def dejar_feromona(recorrido_hormiga):
    # Programa para cargar con feromona cuando una hormiga encuentra el hormiguero
    global feromona

    # Añado una cantidad de feromona en cada casilla
    cantidad_feromona = 1
    for casilla_camino in recorrido_hormiga:
        feromona[casilla_camino]+=cantidad_feromona
    

def pintar_camino(win, recorrido_hormiga):
    # Con esta función quiero pintar el recorrido que ha seguido la hormiga.

    # Utilizo la función range para omitir el primer y último paso, para no pintar
    #   encima del hormiguero o la comida.

        global feromona, feromona_inicial, horm, comi

        color_max = max(feromona)-feromona_inicial
        color_camino1 = (236, 250, 230)
        color_camino2 = (198, 224, 180)
        color_camino3 = (169, 208, 142)
        color_camino4 = (112, 173,  71)

        for celda_a_pintar in range (0,len(feromona)):
            if feromona[celda_a_pintar]== feromona_inicial or celda_a_pintar == horm or celda_a_pintar==comi:
                pass
            elif feromona[celda_a_pintar]<color_max*1/4+feromona_inicial:
                color_camino = color_camino1
                pinto_cuadro(win, color_camino, celda_a_pintar)
            elif feromona[celda_a_pintar]<color_max*2/4+feromona_inicial:
                color_camino = color_camino2
                pinto_cuadro(win, color_camino, celda_a_pintar)
            elif feromona[celda_a_pintar]<color_max*3/4+feromona_inicial:
                color_camino = color_camino3
                pinto_cuadro(win, color_camino, celda_a_pintar)
            else:
                color_camino = color_camino4
                com_pinto_cuadro(win, color_camino, celda_a_pintar)
        
        # paso_hormiga = recorrido_hormiga[celda_a_pintar]

        # pinto_cuadro(win, color_camino, celda_a_pintar)

    # for celda_a_pintar in range (1,len(recorrido_hormiga)-1):
        
    #     paso_hormiga = recorrido_hormiga[celda_a_pintar]
                
    #     color_camino1 = (236, 250, 230)
    #     color_camino2 = (198, 224, 180)
    #     color_camino3 = (169, 208, 142)
    #     color_camino4 = (112, 173,  71)

    #     pinto_cuadro(win, color_camino, paso_hormiga)


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

def obtener_entorno_de_fichero():
    # Función para cargar el entorno de un fichero en vez de generarlo cada vez.
    #   utilizo la función pickle que es muy eficiente
    #   utilizo read binary "rb"
    global entorno

    with open("Datos/DatosEntorno"+str(tamX)+"x"+str(tamY)+".txt", 'rb') as fp:
        entorno = pickle.load(fp)
    
def recuento_de_exitos():
    # Programa para hacer el recuento de exitos y almacenarlos

    global exitos, fracasos, recorrido_corto

    # Calculo las variables derivadas y alimento la lista general
    total_intentos = exitos + fracasos
    exitos_porc = exitos*100 // total_intentos
    fracasos_porc = fracasos*100 // total_intentos
    recorrido_corto_num = len(recorrido_corto)
    track_success = [exitos,fracasos,total_intentos,exitos_porc,"%",fracasos_porc,"%",recorrido_corto_num,recorrido_corto]

    print("Resultados: ", track_success)

def main():
    # Este es el programa principal de Ejecución
    # Tiene algunos trozos de programa, que se podrían delegar fuera, para dejar solo lo principal

    
    
    # Establecer el tamaño de la ventana y lo mete en una variable
    win = pygame.display.set_mode((dispX,dispY))

    # Establecer el título de la ventana
    pygame.display.set_caption("Swarm AI")

    # La pinta de color blanco el fondo
    win.fill((255,255,255))

    # Ejecución de programa
    # Quitar las señales a las partes que quiero ejecutar

    text_on_screen(win)

    # Carga inicial feromona
    carga_inicial_feromona()

    # Carga laberinto
    obtener_entorno_de_fichero() # Este si quiero que lo tome de fichero

    # Defino dónde está el hormiguero y dónde la comida
    # Esto lo tengo que meter en un fichero para poder guardarlo
    horm = com_hormiguero(win,tamY)
    comi = com_comida(win,tamY)

    # Pinto el hormiguero
    com_pintar_hormiguero(bordX,bordY,win)

    # Esto es necesario para que se vea lo que pinto
    pygame.display.update()

    # Saco a pasear un número "n" de hormigas
    numero_de_hormigas = tamX*tamY*1
    # numero_de_hormigas = 1
    for n in range(1,numero_de_hormigas+1):
        # print("Sale la hormiga: ",n," .............suerte!")
        paseo_hormiga1(win,horm,comi)
        pygame.display.update()
    
    # print("Feromona final: ",feromona)

    # Programa que me dice cómo lo estoy haciendo para comparar estrategias
    recuento_de_exitos()

    # Esto es necesario para que se vea lo que pinto
    pygame.display.update()



    # Ejemplo de como mantener un programa corriendo hasta que cambias una variable.
    # Paso 1. Defines la variable
    run = True
    # Paso 2. Mientras no la cambies a False, sigue corriendo en loop
    while run:
        # Esto es necesario para que puedas cerrar la ventana creada pulsando en la X de arriba
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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