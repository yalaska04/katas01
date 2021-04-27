import pygame as pg
import sys 

ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)
ANCHO = 800
ALTO = 600

pg.font.init()
pantalla = pg.display.set_mode((ANCHO,ALTO))

game_over = False
x = ANCHO // 2
y = ALTO // 2
vx = -5
vy = -5
reloj = pg.time.Clock() # creamos la instancia Clock

while not game_over: 
    reloj.tick(60) # el reloj no permite flujo hasta que llega al tiempo establecido (= tapón temporal)
    for evento in pg.event.get(): 
        if evento.type == pg.QUIT: 
            game_over = True 
    
    # Modificación de estado
    x += vx 
    y += vy
  
    if y <= 0 or y >= ALTO: 
        vy = -vy
    
    if x <= 0 or x >= ANCHO:  
        vx = -vx
    
    # Gestión de la pantalla
    pantalla.fill(NEGRO) # rellenamos la pantalla
    pg.draw.circle(pantalla, ROJO, (x, y), 10) # (sup, color, pos, rad)

    pg.display.flip() # refrescar la pantalla 

pg.quit()
sys.exit()