import pygame as pg
import sys 
import random

ANCHO = 800
ALTO = 600
FPS = 60

BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)

class Marcador(pg.sprite.Sprite): 
    def __init__(self, x, y, fontsize=25, color=BLANCO): 
        super().__init__() # llamo al init del sprite. 
        self.fuente = pg.font.SysFont('Arial', fontsize) 
        self.text = '0'
        self.color = color 
        self.image = self.fuente.render(str(self.text), True, self.color)
        self.rect = self.image.get_rect(topleft=(x,y))

    def update(self, dt): 
        self.image = self.fuente.render(str(self.text), True, self.color)

class Raqueta(pg.sprite.Sprite):
    disfraces = ['electric00.png', 'electric01.png', 'electric02.png']

    def __init__(self, x, y, w=100, h=30): 
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.imagen_actual = 0
        self.milisegundos_para_cambiar = 1000 // FPS * 5 # cambie disfraz cada 5 fotogramas
        self.milisegundos_acumulados = 0
        self.image = self.imagenes[self.imagen_actual]
        
        # para que aparezca un rectángulo rojo 
        # self.image = pg.Surface((w,h), pg.SRCALPHA, 32) # pg.SRCALPHA = sup transparente
        # pg.draw.rect(self.image, ROJO, pg.Rect(0, 0, w, h), border_radius=5)

        self.rect = self.image.get_rect(centerx = x, bottom = y)
        self.vx = 7 
    
    def cargaImagenes(self): 
        imagenes = []
        for fichero in self.disfraces: 
            imagenes.append(pg.image.load('./images/{}'.format(fichero)))
        return imagenes

    def update(self, dt): 
        teclas_pulsadas = pg.key.get_pressed()
        if teclas_pulsadas[pg.K_LEFT]: 
            self.rect.x -= self.vx

        if teclas_pulsadas[pg.K_RIGHT]: 
            self.rect.x += self.vx
        
        if self.rect.left <= 0: 
            self.rect.left = 0 
        if self.rect.right >= ANCHO: 
            self.rect.right = ANCHO

        self.milisegundos_acumulados += dt 
        if self.milisegundos_acumulados >= self.milisegundos_para_cambiar:
            self.imagen_actual += 1
            if self.imagen_actual >= len(self.disfraces):
                self.imagen_actual = 0 
            self.milisegundos_acumulados = 0
        self.image = self.imagenes[self.imagen_actual]

class Bola(pg.sprite.Sprite):
    def __init__(self, x, y,):
        super().__init__()
        self.image = pg.image.load('./images/ball1.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))
        self.xOriginal = x
        self.yOriginal = y
        self.estoyViva = True
        self.vx = random.randint(5, 10) * random.choice([-1, 1])
        self.vy = random.randint(5, 10) * random.choice([-1, 1])

    def prueba_colision(self, grupo):
        candidatos = pg.sprite.spritecollide(self, grupo, False)
        if len(candidatos) > 0:
            self.vy *= -1

    def update(self, dt):
        if self.estoyViva:
            self.rect.x += self.vx
            self.rect.y += self.vy
            if self.rect.left <= 0 or self.rect.right >= ANCHO:
                self.vx *= -1 
            if self.rect.top <= 0:
                self.vy *= -1
            if self.rect.bottom >= ALTO:
                self.estoyViva = False
        else:
            self.rect.center = (self.xOriginal, self.yOriginal)
            self.vx = random.randint(5, 10) * random.choice([-1, 1])
            self.vy = random.randint(5, 10) * random.choice([-1, 1])
            self.estoyViva = True

class Game(): 
    def __init__(self): 
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.vidas = 3
        self.todoGrupo = pg.sprite.Group() # instancia de grupo 
        self.grupoJugador = pg.sprite.Group()
        self.grupoLadrillos = pg.sprite.Group()

        self.cuentaSegundos = Marcador(10,10)
        self.todoGrupo.add(self.cuentaSegundos)

        self.bola = Bola(ANCHO //2, ALTO // 2)
        self.todoGrupo.add(self.bola)

        self.raqueta = Raqueta(x = ANCHO//2, y = ALTO - 40)
        self.grupoJugador.add(self.raqueta)
        
        self.todoGrupo.add(self.grupoJugador, self.grupoLadrillos)
        
    def bucle_principal(self):
        game_over = False
        reloj = pg.time.Clock()
        contador_milisegundos = 0 
        segundero = 0

        while not game_over or self.vidas > 0: 
            dt = reloj.tick(FPS)
            contador_milisegundos += dt 

            if contador_milisegundos >= 1000: 
                segundero += 1
                contador_milisegundos = 0 

            for evento in pg.event.get():
                if evento.type == pg.QUIT: 
                    game_over = True
            
            self.cuentaSegundos.text = segundero
            self.bola.prueba_colision(self.grupoJugador)
            self.todoGrupo.update(dt)
            if not self.bola.estoyViva: 
                self.vidas -= 1
            
            self.pantalla.fill(NEGRO)
            self.todoGrupo.draw(self.pantalla)

            pg.display.flip()

if __name__ == '__main__': 
    pg.font.init()
    game = Game()
    game.bucle_principal()