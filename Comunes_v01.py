# Fichero con todas las variables comunes y todos los módulos comunes.

# Variables comunes-------------------------------------

# Tamaño Display
dispX = 1900
dispY = 1010

# Tamaño Bordes. Esto define el borde superior y el izquierdo
# para ver dónde pinta el hormiguero
bordX = 200
bordY = 20

# Fijo el Tamaño para test de las variables principales
tamX = 40
tamY = 20
bordes = 25

# Calculo el tamaño de las casillas para que no se salgan de la pantalla
tcX = (dispX-(bordX+bordY))/tamX
tcY = (dispY-(bordY*2))/tamY
tc = min (tcX, tcY)

# Colores
color_negro = (0, 0, 0)
color_amarillo = (255,255,0)
color_rojo = (255,0,0)


# Módulos comunes---------------------------------------

def com_pintar_hormiguero(bordX,bordY,win,entorno,dispX,dispY,tamX,tamY,tc):
# Utilizando pygame defino una función para pintar el entorno
# Esto lo hice complicado porque estaba en turtle e iba muy lento
# En pygame va rápido por lo que lo puedo simplificar

# Importo lo que me va a hacer falta
    import pygame

# Primero pinto los bordes
   
    for casilla in range(0, tamY):
        casillaCheck = entorno[casilla]
        com_pintar_bordes_casilla(bordX,bordY,casillaCheck,win,dispX,dispY,tc, color_negro)

        casillaCheck = entorno[casilla+tamY*(tamX-1)]
        com_pintar_bordes_casilla(bordX,bordY,casillaCheck,win,dispX,dispY,tc, color_negro)

    for casilla in range(0, tamX-1):
        casillaCheck = entorno[tamY+casilla*tamY]
        com_pintar_bordes_casilla(bordX,bordY,casillaCheck,win,dispX,dispY,tc, color_negro)

        casillaCheck = entorno[tamY*2-1+casilla*tamY]
        com_pintar_bordes_casilla(bordX,bordY,casillaCheck,win,dispX,dispY,tc, color_negro)

# Luego el interior alternando celdas

    for columna in range(0, tamX-2):
        for fila in range(0,tamY//2):
            if columna%2==0:
                tieneQueSerImpar =1
            else:
                tieneQueSerImpar= 0
                
            casillaCheck = entorno[tamY+1+columna*tamY+fila*2+tieneQueSerImpar]
            ## print(columna, fila,casillaCheck,tieneQueSerImpar)

            com_pintar_bordes_casilla(bordX,bordY,casillaCheck,win,dispX,dispY,tc, color_negro)

def com_pintar_bordes_casilla(bordX,bordY,casillaCheck,win,dispX,dispY,tc,color):
    # Programa para pintar los bordes de una casilla determinada
    # Defino el tamaño de las casillas y el origen de cada una

# Importo lo que me va a hacer falta
    import pygame

    posX = casillaCheck[0]*tc+bordX
    posY = casillaCheck[1]*tc+bordY

    # Pintar lados Casilla
    
    if casillaCheck[2]==1:
        pygame.draw.line(win, color, (posX, posY), (posX, posY+tc), 3)

    if casillaCheck[3]==1:
        pygame.draw.line(win, color, (posX, posY+tc), (posX+tc, posY+tc), 3)

    if casillaCheck[4]==1:
        pygame.draw.line(win, color, (posX+tc, posY+tc), (posX+tc, posY), 3)

    if casillaCheck[5]==1:
        pygame.draw.line(win, color, (posX+tc, posY), (posX, posY), 3)

def com_pintar_un_borde(bordX,bordY,casillaCheck,win,dispX,dispY,tc,color,borde):
    # Programa para pintar los bordes de una casilla determinada
    # Defino el tamaño de las casillas y el origen de cada una

# Importo lo que me va a hacer falta
    import pygame

    posX = casillaCheck[0]*tc+bordX
    posY = casillaCheck[1]*tc+bordY

    # Pintar lados Casilla
    
    if borde ==1:
        pygame.draw.line(win, color, (posX, posY), (posX, posY+tc), 3)

    if borde ==2:
        pygame.draw.line(win, color, (posX, posY+tc), (posX+tc, posY+tc), 3)

    if borde==3:
        pygame.draw.line(win, color, (posX+tc, posY+tc), (posX+tc, posY), 3)

    if borde==4:
        pygame.draw.line(win, color, (posX+tc, posY), (posX, posY), 3)


def com_pinto_cuadro (win, color, casilla,entorno, bordX, bordY, tc):
    # Programa para pintar cuadros en el hormiguero

    import pygame

    casilla_pintar = entorno[casilla]
    coord_X = casilla_pintar[0]
    coord_Y = casilla_pintar[1]

    # Para que los cuadrados no tapen los bordes, les quito un 10% de área.
    bordeblanco = tc/10

    # Dibujo el cuadrado
    pygame.draw.rect(win, color, (coord_X*tc+bordX+bordeblanco,coord_Y*tc+bordY+bordeblanco, tc-bordeblanco*2, tc-bordeblanco*2), 0)


def com_hormiguero(win,entorno,tamY,bordX,bordY,tc):
    # Programa para situar el hormiguero

    global horm

    # Selecciono origen hormiguero aleatorio (tengo que cambiar por el tema de los bordes)
    # horm = random.randint(0,len(entorno)-1)

    # Fijo el hormiguero en un punto fijo
    horm = 2*tamY+tamY//2

    # print ("Hormiguero en: ",horm)
    # print (entorno[horm])
    
    color_hormiguero = (201, 135, 58)

    com_pinto_cuadro(win, color_hormiguero, horm,entorno, bordX, bordY, tc)

    return horm

def com_comida(win,entorno,tamY,bordX,bordY,tc):
    # Programa para situar la comida

    global comi

    # Selecciono origen hormiguero aleatorio (tengo que cambiar por el tema de los bordes)
    # comi = random.randint(0,len(entorno)-1)

    # Fijo la comida en un punto fijo
    comi = len(entorno)-(2*tamY+tamY//2)

    # print ("Comida en: ",comi)
    # print (entorno[comi])
    
    color_comida = (91, 155, 213)

    com_pinto_cuadro(win, color_comida, comi,entorno, bordX, bordY, tc)

    return comi

def com_text_on_screen(win,tamX,tamY):
    # Este es el programa que escribe en la pantalla

    import pygame

    # Dibujo el fondo
    win.fill((221,221,221))

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

    # Dibujamos botón Exit
    botonExit = pygame.Surface((100,25))
    botonExit.fill((255,0,0))
    win.blit(botonExit,(20,120))
    textExit = fontB.render("Exit", True, 0)
    win.blit(textExit, (25, 125))

    # Dibujamos botón Otro Laberinto
    botonOtro = pygame.Surface((100,25))
    botonOtro.fill((198,224,180))
    win.blit(botonOtro,(20,160))
    textOtro = fontB.render("Otro", True, 0)
    win.blit(textOtro, (25, 165))


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

def com_borrar_hormiguero(win,dispX,dispY,bordX,bordY):
    # Programa para borrar lo que hay pintado
    
    import pygame

    longX = dispX-bordX
    longY = dispY-bordY
    fondoHormiguero = pygame.Surface((longX,longY))
    fondoHormiguero.fill((221,221,221))
    win.blit(fondoHormiguero,(bordX,bordY))