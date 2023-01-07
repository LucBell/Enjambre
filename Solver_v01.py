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

# Saco a pasear un número "n" de hormigas
aguante_hormiga = (tamX+tamY)*6
# aguante_hormiga = 1
numero_de_hormigas = tamX*tamY*10
# numero_de_hormigas = 1
pausa_hormigas = 3

# Calculo el tamaño de las casillas para que no se salgan de la pantalla
tcX = (dispX-(bordX+bordY))/tamX
tcY = (dispY-(bordY*2))/tamY
tc = min (tcX, tcY)

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

def paseo_hormiga1(win,horm,comi):
    # Hormiga que pasea por el hormiguero y que cuando encuentra la comida,
    # vuelve marcando las casillas como "comida encontrada"
    # también tiene que levantar muros si se encuentra casillas bloqueadas

    # Carga variables globales
    global entorno
    global exitos, fracasos, recorrido_corto, aguante_hormiga

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

                # Si da la casualidad que está la comida en la plaza anulo el eliminar la plaza
                if celda_anexa_delante == entorno[comi]:
                    bordes_plaza_dcha =1
                    bordes_plaza_izda = 1

            if bordes_plaza_izda ==0 or bordes_plaza_dcha ==0:
                # Si detecto plaza, levanto un muro delante (como si hubiese un callejón delante)
                print("Plaza detectada!!")
                print("Celda anexa delante: ", celda_anexa_delante)
                print("Comi: ", entorno[comi])
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
    com_pintar_bordes_casilla(bordX,bordY,casilla,win,dispX,dispY,tc)
    
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
                com_pinto_cuadro(win, color_camino, celda_a_pintar,entorno, bordX, bordY, tc)
            elif feromona[celda_a_pintar]<color_max*2/4+feromona_inicial:
                color_camino = color_camino2
                com_pinto_cuadro(win, color_camino, celda_a_pintar,entorno, bordX, bordY, tc)
            elif feromona[celda_a_pintar]<color_max*3/4+feromona_inicial:
                color_camino = color_camino3
                com_pinto_cuadro(win, color_camino, celda_a_pintar,entorno, bordX, bordY, tc)
            else:
                color_camino = color_camino4
                com_pinto_cuadro(win, color_camino, celda_a_pintar,entorno, bordX, bordY, tc)

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

def inicio(win):
    # Programa que limpia la pantalla, carga de nuevo el entorno
    # y lanza las hormigas a buscar la comida

    global entorno
    entorno = []
    feromona = []

    # Borro el hormiguero pintando encima
    com_borrar_hormiguero(win,dispX,dispY,bordX,bordY)

    # Carga inicial feromona
    carga_inicial_feromona()

    # Carga laberinto
    obtener_entorno_de_fichero()

    # Defino dónde está el hormiguero y dónde la comida
    # Esto lo tengo que meter en un fichero para poder guardarlo
    global horm, comi
    horm = com_hormiguero(win,entorno,tamY,bordX,bordY,tc)
    comi = com_comida(win,entorno,tamY,bordX,bordY,tc)

    # Pinto el hormiguero
    com_pintar_hormiguero(bordX,bordY,win,entorno,dispX,dispY,tamX,tamY,tc)

    # Esto es necesario para que se vea lo que pinto
    pygame.display.update()

    # Paro el programa para ver el laberito antes de que se modifique
    print("Paramos un momento...")
    time.sleep(pausa_hormigas)
    print("Salen las hormigas!")

    for n in range(1,numero_de_hormigas+1):
        # print("Sale la hormiga: ",n," .............suerte!")
        paseo_hormiga1(win,horm,comi)
        pygame.display.update()
    
    # print("Feromona final: ",feromona)

    # Programa que me dice cómo lo estoy haciendo para comparar estrategias
    recuento_de_exitos()

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

    com_text_on_screen(win,tamX,tamY)

    inicio(win)

    # Ejemplo de como mantener un programa corriendo hasta que cambias una variable.
    # Paso 1. Defines la variable
    run = True
    # Paso 2. Mientras no la cambies a False, sigue corriendo en loop
    while run:
        # Aquí registro los eventos que me interesan:
        # Pulsar en la x de la ventana para cerrarla
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pygame.mouse.get_pos()
        # Pulsar en el botón de otra vez        
                if 20 <= x_mouse <= 120 and 160 <= y_mouse <= 185:
                    # este lo guardo para otros botones
                    inicio(win)
        # Pulsar en el boton de salida
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