import pygame as pg
import sys
from random import randint

def rebotaX(x): 
    if x <= 0 or x >= ANCHO: 
        return -1
    return 1

def rebotaY(y): 
    if y <= 0 or y >= ALTO: 
        return -1
    return 1

ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)
ANCHO = 800
ALTO = 600

pg.font.init()
pantalla = pg.display.set_mode((ANCHO,ALTO))
reloj = pg.time.Clock() # creamos la instancia Clock

bolas = []
for _ in range(10): 
    bola = {'x': randint(0, ANCHO),
            'y': randint(0, ALTO),
            'vx': randint(5,10),
            'vy': randint(5,10),
            'color': (randint(0,255), randint(0,255), randint(0, 255)),
    }
    bolas.append(bola)
# Bola 1
x = ANCHO // 2
y = ALTO // 2
vx = -7
vy = -7

# Bola 2
x2 = randint(0, ANCHO)
y2 = randint(0, ALTO)
vx2 = randint(5,15)
vy2 = randint(5,15)

game_over = False
while not game_over: 
    reloj.tick(60) # el reloj no permite flujo hasta que llega al tiempo establecido (= tapón temporal)

    # Gestión de eventos
    for evento in pg.event.get(): 
        if evento.type == pg.QUIT: 
            game_over = True 
    
    # Modificación de estado

    for bola in bolas: 
        bola['x'] += bola['vx']
        bola['y'] += bola['vy']
    
        bola['vy'] *= rebotaY(bola['y'])
        bola['vx'] *= rebotaX(bola['x'])
    
    # Gestión de la pantalla
    pantalla.fill(NEGRO) # rellenamos la pantalla
    for bola in bolas: 
        pg.draw.circle(pantalla, bola['color'], (bola['x'], bola['y']), 10)# (sup, color, pos, rad)
        
    pg.display.flip() # refrescar la pantalla 

pg.quit()
sys.exit()