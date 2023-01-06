
def com_pintar_hormiguero(origenX,origenY,win):
    
# Utilizando pygame defino una función para pintar el entorno
# Esto lo hice complicado porque estaba en turtle e iba muy lento
# En pygame va rápido por lo que lo puedo simplificar

# Primero pinto los bordes
   
    for casilla in range(0, tamY):
        casillaCheck = entorno[casilla]
        com_pintar_bordes_casilla(origenX,origenY,casillaCheck,win)

        casillaCheck = entorno[casilla+tamY*(tamX-1)]
        com_pintar_bordes_casilla(origenX,origenY,casillaCheck,win)

    for casilla in range(0, tamX-1):
        casillaCheck = entorno[tamY+casilla*tamY]
        com_pintar_bordes_casilla(origenX,origenY,casillaCheck,win)

        casillaCheck = entorno[tamY*2-1+casilla*tamY]
        com_pintar_bordes_casilla(origenX,origenY,casillaCheck,win)

# Luego el interior alternando celdas

    for columna in range(0, tamX-2):
        for fila in range(0,tamY//2):
            if columna%2==0:
                tieneQueSerImpar =1
            else:
                tieneQueSerImpar= 0
                
            casillaCheck = entorno[tamY+1+columna*tamY+fila*2+tieneQueSerImpar]
            ## print(columna, fila,casillaCheck,tieneQueSerImpar)

            com_pintar_bordes_casilla(origenX,origenY,casillaCheck,win)

def com_pintar_bordes_casilla(origenX,origenY,casillaCheck,win):
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


def com_pinto_cuadro (win, color, casilla):

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


def com_hormiguero(win,tamY):
    # Programa para situar el hormiguero

    global horm

    # Selecciono origen hormiguero aleatorio (tengo que cambiar por el tema de los bordes)
    # horm = random.randint(0,len(entorno)-1)

    # Fijo el hormiguero en un punto fijo
    horm = 2*tamY+tamY//2

    print ("Hormiguero en: ",horm)
    print (entorno[horm])
    
    color_hormiguero = (201, 135, 58)

    com_pinto_cuadro(win, color_hormiguero, horm)

    return horm

def com_comida(win,tamY):
    # Programa para situar la comida

    global comi

    # Selecciono origen hormiguero aleatorio (tengo que cambiar por el tema de los bordes)
    # comi = random.randint(0,len(entorno)-1)

    # Fijo el hormiguero en un punto fijo
    comi = len(entorno)-1-(2*tamY+tamY//2)

    # print ("Comida en: ",comi)
    # print (entorno[comi])
    
    color_comida = (91, 155, 213)

    com_pinto_cuadro(win, color_comida, comi)

    return comi



def com_text_on_screen(win):

    

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


def com_obtener_entorno_de_fichero():
    # Función para cargar el entorno de un fichero en vez de generarlo cada vez.
    #   utilizo la función pickle que es muy eficiente
    #   utilizo read binary "rb"
    global entorno

    with open("Datos/DatosEntorno.txt", 'rb') as fp:
        entorno = pickle.load(fp)

