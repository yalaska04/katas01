# Mi intento de las bolas que rebotan 
import pygame as pg
import sys
from random import randint

ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)
ANCHO = 800
ALTO = 600
VAL_VELOCIDAD = [randint(-10, -5), randint(5, 10)]

class Bola(): 
    def __init__(self, x, y, vx, vy, color): 
        # Creo mis atributos 
        self.x = x
        self.y = y 
        self.vx = vx
        self.vy = vy 
        self.color = color 

    def tocaBordeX(self, x):
        if self.x <= 0 or self.x >= ANCHO: 
            return -1
        return 1
    
    def tocaBordeY(self, y):
        if self.y <= 0 or self.y >= ALTO: 
            return -1
        return 1

class Game(): 
    bolas = []
    def __init__(self):
        self.pantalla = pg.display.set_mode((ANCHO,ALTO))
        self.reloj = pg.time.Clock() # creamos la instancia Clock

        for _ in range(10): 
            bola = Bola(randint(0, ANCHO),
                        randint(0, ALTO),
                        VAL_VELOCIDAD[randint(0,1)],
                        VAL_VELOCIDAD[randint(0,1)],
                        (randint(0, 255), randint(0, 255), randint(0, 255)))

            self.bolas.append(bola)

    def cerrar(self):
        pg.quit()
        sys.exit()
    
    def rebotar(self):
        game_over = False
        while not game_over: 
            self.reloj.tick(60) # el reloj no permite flujo hasta que llega al tiempo establecido (= tapón temporal)

            # Gestión de eventos
            for evento in pg.event.get(): 
                if evento.type == pg.QUIT: 
                    game_over = True 
            
            # Modificación de estado

            for bola in self.bolas: 
                bola.x += bola.vx
                bola.y += bola.vy
            
                bola.vy *= bola.tocaBordeY(bola.x)
                bola.vx *= bola.tocaBordeX(bola.y)
            
            # Gestión de la pantalla
            self.pantalla.fill(NEGRO) # rellenamos la pantalla
            for bola in self.bolas: 
                pg.draw.circle(self.pantalla, bola.color, (bola.x, bola.y), 10)# (sup, color, pos, rad)
                
            pg.display.flip() # refrescar la pantalla 

        self.cerrar()

if __name__ == '__main__':
    game = Game()
    pg.font.init()
    game.rebotar()