import pygame as pg
import sys
from random import randint, choice

BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)
ANCHO = 800
ALTO = 600

pg.font.init()
pantalla = pg.display.set_mode((ANCHO,ALTO))
pg.display.set_caption("Rebota Bola")
miFont = pg.font.SysFont("monospace", 16)
reloj = pg.time.Clock() # creamos la instancia Clock

class Bola():
    def __init__(self, x, y, vx=5, vy=5, color=(255,255,255), radio = 7): 
        # Creo mis atributos 
        self.x = x
        self.y = y 
        self.vx = vx
        self.vy = vy 
        self.color = color
        self.anchura = radio*2
        self.altura = radio*2

    def actualizar(self):

        self.x += self.vx
        self.y += self.vy

        if self.x <= 0 or self.x >= ANCHO: 
            self.vx = -self.vx
 
        if self.y <= 0: 
            self.vy = -self.vy

        if self.y >= ALTO: 
            self.x = ANCHO // 2
            self.y = ALTO // 2
            self.vx = randint(5,10)*choice([-1,1])
            self.vy = randint(5,10)*choice([-1,1])
            return True
        return False
    
    def dibujar(self, lienzo): 
        pg.draw.circle(lienzo, self.color, (self.x, self.y), self.anchura//2) # (sup, color, pos, rad)

    def comprueba_colision(self, objeto):
        choqueX = self.x >= objeto.x and self.x <= objeto.x + objeto.anchura or \
            self.x + self.anchura >= objeto.x and self.x + self.anchura <= objeto.x + objeto.anchura
              
        '''
        Es lo mismo que decir: 
        if self.x >= objeto.x and self.x <= objeto.x + objeto.anchura or \
            self.x + self.anchura >= objeto.x and self.x + self.anchura <= objeto.x + objeto.anchura:
            choqueX = True
        '''
        
        choqueY = self.y>= objeto.y and self.y <= objeto.y + objeto.altura or \
            self.y + self.altura >= objeto.y and self.y + self.altura <= objeto.y + objeto.altura
        
        if choqueX and choqueY: # para que haya colisión los dos choques tienen que ser True
            self.vy *= -1
    
    def comprueba_colision2(self, objeto): 
        choqueX = self.x >= objeto.x and self.x <= objeto.x + objeto.anchura or \
            self.x + self.anchura >= objeto.x and self.x + self.anchura <= objeto.x + objeto.anchura
        choqueY = self.y>= objeto.y and self.y <= objeto.y + objeto.altura or \
            self.y + self.altura >= objeto.y and self.y + self.altura <= objeto.y + objeto.altura

        if choqueX and choqueY:
            return True 
        return False
   
class Raqueta():
    def __init__(self, x=0, y=0):
        self.altura = 23
        self.anchura = 100
        self.color = (255, 255, 255)
        self.x = (ANCHO - self.anchura)// 2
        self.y = ALTO - self.altura - 15
        self.vx = 13
        self.vy = 0 
    
    def dibujar(self,lienzo): 
        rect = pg.Rect(self.x, self.y, self.anchura, self.altura)
        pg.draw.rect(lienzo, self.color, rect)

    def actualizar(self):
        teclas_pulsadas = pg.key.get_pressed()
        if teclas_pulsadas[pg.K_LEFT] and self.x > 0:
            self.x -= self.vx

        if teclas_pulsadas[pg.K_RIGHT] and self.x < ANCHO - self.anchura:
            self.x += self.vx 

vidas = 5
puntos = 0 

bola = Bola(randint(0,ANCHO),
            randint(0,ALTO),
            randint(5,10) * choice([-1,1]),
            randint(5,10) * choice([-1,1]),
            (randint(0,255), randint(0,255), randint(0,255)))

raqueta = Raqueta()

game_over = False
while not game_over: 
    reloj.tick(60) # el reloj no permite flujo hasta que llega al tiempo establecido (= tapón temporal)

    # Gestión de eventos
    for evento in pg.event.get(): 
        if evento.type == pg.QUIT: 
            game_over = True 

    if vidas > 0: 
        # Modificación de estado
        raqueta.actualizar()

        pierdeBola = bola.actualizar()
        if pierdeBola: 
            vidas -= 1

        bola.comprueba_colision(raqueta)
        haChocado = bola.comprueba_colision2(raqueta)
        if haChocado: 
            puntos += 5

        # Gestión de la pantalla
        pantalla.fill(NEGRO) # rellenamos la pantalla
        bola.dibujar(pantalla)
        raqueta.dibujar(pantalla)

        puntosText = miFont.render('Puntos {}'.format(puntos), 1, BLANCO) # Font.render(text, antialias, color, background)
        pantalla.blit(puntosText, (20,20))

        vidasText = miFont.render('Vidas {}'.format(vidas), 1, BLANCO) 
        pantalla.blit(vidasText, (700,20))

        # pg.display.flip() # refrescar la pantalla 
        if pierdeBola:
            pg.time.delay(500) #para que haga el delay con la bola en el centro de pantalla
    
    else: 
        pantalla.fill(NEGRO)
        FinDeJuego = miFont.render('GAME OVER', 1, ROJO)
        pantalla.blit(FinDeJuego, (ANCHO // 2 - 50, ALTO // 2 - 20))
        
        PuntosFinales = miFont.render('Puntos: {}'.format(puntos), 1, BLANCO)
        pantalla.blit(PuntosFinales, (ANCHO // 2 - 50, ALTO // 2))
        
    pg.display.flip() # hay que intentar que solo haya un pg.display.flip()

pg.quit()
sys.exit()
