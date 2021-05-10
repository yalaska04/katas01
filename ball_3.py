import pygame as pg
import sys 
import random
from enum import Enum

ANCHO = 800
ALTO = 600
FPS = 60

BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)

level1 = ['XXXXXXXX',
              'X--DD--X',
              'X--DD--X',
              'XXXXXXXX']
              
class MarcadorH(pg.sprite.Sprite): 
    # Marcador versión Hugo, usando diccionarios y párametro clave-valor
    plantilla = '{}'

    def __init__(self, x, y, justificado='topleft', fontsize=25, color=BLANCO): 
        super().__init__() # llamo al init del sprite. 
        self.fuente = pg.font.SysFont('Arial', fontsize) 
        self.text = '0'
        self.color = color 
        self.justificado = justificado
        self.image = self.fuente.render(str(self.text), True, self.color)
        self.x = x 
        self.y = y

    def update(self, dt): 
        self.image = self.fuente.render(self.plantilla.format(self.text), True, self.color)
        d = {self.justificado: (self.x, self.y)}
        self.rect = self.image.get_rect(**d)

class CuentaVidas(MarcadorH): 
    plantilla = 'Vidas: {}'

class Ladrillo(pg.sprite.Sprite): 
    disfraces = ['greenTile.png', 'redTile.png', 'redTileBreak.png'] 
    def __init__(self, x, y, esDuro=False): 
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.esDuro = esDuro
        self.imagen_actual = 1 if self.esDuro else 0 # operador ternario: if en una sola línea
        self.image = self.imagenes[self.imagen_actual]
        self.rect = self.image.get_rect(topleft=(x,y))
        self.numGolpes = 0 

        if  self.esDuro == None: 
            self.image = None

    def cargaImagenes(self): 
        imagenes = []
        for fichero in self.disfraces: 
            imagenes.append(pg.image.load('./images/{}'.format(fichero)))
        return imagenes

    def update(self, dt): 

        if self.esDuro and self.numGolpes == 1: 
            self.imagen_actual = 2 
            self.image = self.imagenes[self.imagen_actual]

    def desaparece(self): 
        # blandos se van con un toque/ duros con dos 
        self.numGolpes += 1
        return (self.numGolpes > 0 and not self.esDuro) or (self.numGolpes > 1 and self.esDuro)
        '''
        es equivalente
        if (self.numGolpes > 0 and not self.esDuro) or (self.numGolpes > 1 and self.esDuro):
            return True
        else: 
            return False
        '''

class Disponer_ladrillos():  

    class Tipo():
        hueco = '-'
        normal = 'X'
        duro = 'D'
    
    def tipo_ladrillos():
        lista = []
        for i in range(4):
            for j in range(8): 
                if level1[i][j] == Disponer_ladrillos.Tipo.hueco:
                    lista.append(None)
                elif level1[i][j] == Disponer_ladrillos.Tipo.normal:
                    lista.append(False)
                elif level1[i][j] == Disponer_ladrillos.Tipo.duro:
                    lista.append(True)
        return lista

class Marcador(pg.sprite.Sprite): 

    class Justificado(): 
        izquierda = 'I'
        derecha = 'D'
        centrado = 'C'

    def __init__(self, x, y, justificado=None, fontsize=25, color=BLANCO): 
        super().__init__() # llamo al init del sprite. 
        self.fuente = pg.font.SysFont('Arial', fontsize) 
        self.text = '0'
        self.color = color 
        self.x = x 
        self.y = y
        if not justificado: 
            self.justificado = Marcador.Justificado.izquierda
        else: 
            self.justificado = justificado

        self.image = self.fuente.render(str(self.text), True, self.color)

    def update(self, dt): 
        self.image = self.fuente.render(str(self.text), True, self.color)
        if self.justificado == Marcador.Justificado.izquierda: 
            self.rect = self.image.get_rect(topleft=(self.x,self.y))
        elif self.justificado == Marcador.Justificado.derecha:
            self.rect = self.image.get_rect(topright=(self.x,self.y))
        else: 
            self.rect = self.image.get_rect(midtop=(self.x,self.y))

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
    disfraces = ['ball1.png', 'ball2.png', 'ball3.png', 'ball4.png', 'ball5.png']

    class Estado_Bola(Enum): 
        viva = 0 
        agonizando = 1
        muerta = 2

    def __init__(self, x, y,):
        super().__init__()
        self.imagenes = self.cargaImagenes()
        self.imagen_actual = 0 # primera imagen (ball1.png)
        self.image = self.imagenes[self.imagen_actual]
        self.milisegundos_acumulados = 0 
        self.milisegundos_para_cambiar = 1000 // FPS * 10

        self.rect = self.image.get_rect(center=(x,y))
        self.xOriginal = x
        self.yOriginal = y
        self.estoyViva = True
        self.estado = Bola.Estado_Bola.viva

        self.vx = random.randint(5, 10) * random.choice([-1, 1])
        self.vy = random.randint(5, 10) * random.choice([-1, 1])
    
    def cargaImagenes(self): 
        imagenes = []
        for fichero in self.disfraces: 
            imagenes.append(pg.image.load('./images/{}'.format(fichero)))
        return imagenes

    def prueba_colision(self, grupo):
        candidatos = pg.sprite.spritecollide(self, grupo, False)
        if len(candidatos) > 0:
            self.vy *= -1
        return candidatos # lista de ladrillos tocados 

    def update(self, dt):
        if self.estado == Bola.Estado_Bola.viva:
            self.rect.x += self.vx
            self.rect.y += self.vy
            if self.rect.left <= 0 or self.rect.right >= ANCHO:
                self.vx *= -1 
            if self.rect.top <= 0:
                self.vy *= -1
       
            if self.rect.bottom >= ALTO:
                self.estado = Bola.Estado_Bola.agonizando
                self.rect.bottom = ALTO

        elif self.estado == Bola.Estado_Bola.agonizando: 
            self.milisegundos_acumulados += dt
            if self.milisegundos_acumulados >= self.milisegundos_para_cambiar:
                self.imagen_actual += 1
                self.milisegundos_acumulados = 0 
                if self.imagen_actual >= len(self.disfraces): 
                    self.estado = Bola.Estado_Bola.muerta
                    self.imagen_actual = 0 
                self.image = self.imagenes[self.imagen_actual]

        else:
            self.rect.center = (self.xOriginal, self.yOriginal)
            self.vx = random.randint(5, 10) * random.choice([-1, 1])
            self.vy = random.randint(5, 10) * random.choice([-1, 1])
            self.estado = Bola.Estado_Bola.viva

class Game(): 
    def __init__(self): 
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.vidas = 10
        self.puntuacion = 0 
        self.todoGrupo = pg.sprite.Group() # instancia de grupo 
        self.grupoJugador = pg.sprite.Group()
        self.grupoLadrillos = pg.sprite.Group()
        
        self.nivel = Disponer_ladrillos.tipo_ladrillos() #lista con True/False/None

        elemento_lista = 0
        for fila in range(4): 
            for columna in range(8): 
                x = columna * 100 + 5 # hay que dibujarse la pantalla para sacar el patrón
                y = fila * 40 + 5
                esDuro = self.nivel[elemento_lista]
                # esDuro = random.randint(1,10) == 1 --> con esto salen ladrillos duros aleatorios
                ladrillo = Ladrillo(x, y, esDuro)
                self.grupoLadrillos.add(ladrillo)
                
                elemento_lista += 1

        self.cuentaPuntos = MarcadorH(10,10, fontsize=50)
        self.cuentaVidas = CuentaVidas(790, 10, 'topright', 50, AMARILLO)
        # self.cuentaVidas = MarcadorH(700, 10, 'topright')
        # self.cuentaVidas = Marcador(700, 10, Marcador.Justificado.derecha)
        self.fondo = pg.image.load('./images/background.png')

        self.bola = Bola(ANCHO //2, ALTO // 2)
        self.todoGrupo.add(self.bola)

        self.raqueta = Raqueta(x = ANCHO//2, y = ALTO - 40)
        self.grupoJugador.add(self.raqueta)
        
        self.todoGrupo.add(self.grupoJugador, self.grupoLadrillos)
        self.todoGrupo.add(self.cuentaPuntos, self.cuentaVidas)
        
    def bucle_principal(self):
        game_over = False
        reloj = pg.time.Clock()

        while not game_over and self.vidas > 0: 
            dt = reloj.tick(FPS)

            for evento in pg.event.get():
                if evento.type == pg.QUIT: 
                    game_over = True
            
            self.cuentaPuntos.text = self.puntuacion
            self.cuentaVidas.text = self.vidas
            self.bola.prueba_colision(self.grupoJugador)
            tocados = self.bola.prueba_colision(self.grupoLadrillos)
            for ladrillo in tocados:
                self.puntuacion += 5
                if ladrillo.desaparece(): 
                    self.grupoLadrillos.remove(ladrillo)
                    self.todoGrupo.remove(ladrillo)


            self.todoGrupo.update(dt)
            if self.bola.estado == Bola.Estado_Bola.muerta: 
                self.vidas -= 1
            
            self.pantalla.blit(self.fondo, (0,0))
            self.todoGrupo.draw(self.pantalla)

            pg.display.flip()

if __name__ == '__main__': 
    pg.font.init()
    game = Game()
    game.bucle_principal()