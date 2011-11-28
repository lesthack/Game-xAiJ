import pygame
import sys
import random

from pygame.locals import *
from data import *
from Ball import *
from Barr import *
from Blocks import *
from Cube import *


markup = (20,20,780,480)

class Ball:
    global markup
    def __init__(self, r, velocity=10):
        self.x = int(random.randrange(markup[0], markup[2]))
        self.y = int(random.randrange(markup[1], markup[3]))
        self.dx = self.dy = self.velocity = int(random.randrange(1,velocity)) 
        self.r = r
        self.color = (int(random.randrange(1,255)),int(random.randrange(1,255)),int(random.randrange(1,255)))
        
    def move(self):
        if self.x >= markup[2]-self.r: self.dx = -self.velocity
        if self.y >= markup[3]-self.r: self.dy = -self.velocity
        if self.x <= markup[0]+self.r: self.dx = self.velocity
        if self.y <= markup[1]+self.r: self.dy = self.velocity
        self.x += self.dx
        self.y += self.dy
        
class Jugador:
    def __init__(self):
        self.nombre = "Player1"
        self.puntaje = 0

class Fire:
    global markup
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 5
        self.h = 30
        
    def move(self):
        self.y -= 10
        
class world:
    global markup
    def __init__(self, Surface):
        self.Surface = Surface
        
        #opcion selecionada
        self.selection = 0
        
        #nivel o mundo actual
        self.level = 0
        
        #jugador
        self.myjugador = Jugador()
        
        #balls
        self.myballs = []
        
        #disparos
        self.myfires = []
        #limite de disparos
        self.limfires = 0
        
        #barra manejada por el mouse
        self.mybarr = Barr(30,markup[3]+10)
        self.mynave = pygame.image.load(filepath("ShipDisplay.png"))
        
        #tiempo (segundos, centecimos)
        self.tiempo = [0,0]
        
        #barreras
        self.mybocks = Blocks()
        self.mycubes = []
        
        #sonido
        pygame.mixer.init()
        pygame.mixer.music.load(filepath("background.ogg"))
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)
        
        self.popSound = pygame.mixer.Sound(filepath("pop.wav"))
        self.laserSound = pygame.mixer.Sound(filepath("laser.wav"))
        self.laserSound.set_volume(0.2)
        
    def createBalls(self, r, c=10, v=1):
        #Crea los objetivos
        for i in range(c):
            self.myballs.append(Ball(r,v))
    
    def paintCubes(self):
        self.mycubes = []
        
        if self.level in self.mybocks.level.keys():
            for block in self.mybocks.level[self.level]:
                self.mycubes.append(Cube(block))
        

    def Draw(self):
        self.paintBackground()
        
        if self.level == 0:
            self.genesys()
        elif self.level == -1:
            self.ayuda()
        elif self.level >= 1:
            self.subBackground()
            self.balls()
            self.barr()
            self.fire()
            self.cube()
            self.isIntercepted()
        
        
    def paintBackground(self):
        pygame.draw.rect(self.Surface, (0,0,0), (10,10,780,580))
    
    def genesys(self):
        #Titulo
        titlefont = pygame.font.Font(filepath(FONT_NAME), 120)
        texto = titlefont.render("xAiJ", True, (250, 250, 250))
        self.Surface.blit(texto, (300,200))
        
        #opciones
        opText = pygame.font.Font(filepath(FONT_NAME), 30)
        txtOption1 = opText.render("Iniciar", True, (250,250,250))
        txtOption2 = opText.render("Ayuda", True, (250,250,250))
        txtSelect = opText.render(">", True, (250,250,100))
        
        self.Surface.blit(txtOption1, (450,350))
        self.Surface.blit(txtOption2, (450,390))
        
        if(self.selection==1):
            y = 390
        elif(self.selection==0):
            y = 350
            
        self.Surface.blit(txtSelect, (420,y))
    
    def subBackground(self):
        pygame.draw.lines(self.Surface, (0,0,250), True, ((markup[0],markup[1]),(markup[2],markup[1]),(markup[2],markup[3]),(markup[0],markup[3])), 5)
        myfont = pygame.font.SysFont("FreeSans", 30)
        texto = myfont.render(":: Puntaje ::", True, (250, 250, 250))
        self.Surface.blit(texto, (25,510))
         
        yourfont = pygame.font.Font(filepath(FONT_NAME), 30)
        texto = yourfont.render(">> %s:" % self.myjugador.nombre, True, (200,0,0))
        self.Surface.blit(texto, (40, 530))
    
        texto = yourfont.render("%s" % self.myjugador.puntaje, True, (200,0,0))
        self.Surface.blit(texto, (220, 530))
         
        texto = yourfont.render("Nivel: %s" % (self.level-1), True, (200,0,0))
        self.Surface.blit(texto, (320, 530))
        
        if self.tiempo[1]>= 1000:
            self.tiempo[0] += 1
            self.tiempo[1] = 0
        else:
            self.tiempo[1]+=9
            
        tiempo = pygame.font.Font(filepath(FONT_NAME), 20)
        texto = tiempo.render("Tiempo: %s.%s" % (self.tiempo[0], self.tiempo[1]), True, (0,50,100))
        self.Surface.blit(texto, (600, 550))
        
    
    def cube(self):
        for mycube in self.mycubes:
            pygame.draw.rect(self.Surface, (85,107,47), (mycube.x, mycube.y, mycube.z, mycube.w))
    
    def balls(self):
        for myball in self.myballs:
            pygame.draw.circle(self.Surface, myball.color, (myball.x, myball.y), myball.r)
            myball.move()
    
    def barr(self):
        self.Surface.blit(self.mynave, (self.mybarr.x + 24, self.mybarr.y-10))
        #pygame.draw.rect(self.Surface, (0,100,100), (self.mybarr.x,self.mybarr.y,self.mybarr.z,self.mybarr.w))
        

    def fire(self):
        for fire in self.myfires:
            pygame.draw.rect(self.Surface, (255,0,0), (fire.x, fire.y, fire.w, fire.h))
            if(fire.y>markup[1]):
                fire.move()
            else:
                self.myfires.remove(fire)
                
    def isIntercepted(self):
        for myball in self.myballs:
            for myfire in self.myfires:
                if (myfire.x >= myball.x and myfire.x <= (myball.x + myball.r)  and myball.y > myfire.y):
                    self.myjugador.puntaje += 1 #ha matado un objetivo
                    self.myballs.remove(myball)
                    self.myfires.remove(myfire)
                    self.popSound.play()
                    return
                
        for myball in self.myballs:
            for mycube in self.mycubes:
                a = myball.x + myball.r >= mycube.x and myball.x + myball.r <= mycube.x + mycube.z and (myball.y + myball.r == mycube.y)
                b = myball.x - myball.r >= mycube.x and myball.x - myball.r <= mycube.x + mycube.z and (myball.y + myball.r == mycube.y)
                c = myball.x + myball.r >= mycube.x and myball.x + myball.r <= mycube.x + mycube.z and (myball.y - myball.r == mycube.y + mycube.w)
                d = myball.x - myball.r >= mycube.x and myball.x - myball.r <= mycube.x + mycube.z and (myball.y - myball.r == mycube.y + mycube.w)
                
                e = myball.y + myball.r >= mycube.y and myball.y + myball.r <= mycube.y + mycube.w and (myball.x + myball.r == mycube.x)
                f = myball.y - myball.r >= mycube.y and myball.y - myball.r <= mycube.y + mycube.w and (myball.x + myball.r == mycube.x)
                g = myball.y + myball.r >= mycube.y and myball.y + myball.r <= mycube.y + mycube.w and (myball.x - myball.r == mycube.x + mycube.z)
                h = myball.y - myball.r >= mycube.y and myball.y - myball.r <= mycube.y + mycube.w and (myball.x - myball.r == mycube.x + mycube.z)
                
                if(a or b):
                    myball.dy = -myball.velocity
                if(c or d):
                    myball.dy = myball.velocity
                if(e or f):
                    myball.dx = -myball.velocity
                if(g or h):
                    myball.dx = myball.velocity
        
        for mycube in self.mycubes:
            for myfire in self.myfires:
                if myfire.x >= mycube.x and myfire.x <= (mycube.x + mycube.z)  and mycube.y >= myfire.y - myfire.h:
                    self.myfires.remove(myfire)
                    return
                
        if self.myballs.__len__() == 0:
            if(self.level<=15):
                self.paintCubes()
                self.level += 1
                self.limfires += 1
                self.createBalls(21-self.level,self.level*10, 2)
                
                
                
                
                
    def ayuda(self):
        titlefont = pygame.font.Font(filepath(FONT_NAME), 40)
        texto = titlefont.render("ayuda ::", True, (250, 250, 250))
        self.Surface.blit(texto, (600,100))
        
        normalfont = pygame.font.Font(filepath(FONT_NAME), 14)
        texto = normalfont.render("xAiJ es un game estrategico lorum lipsum as lorum lipsum as lorum lipsum as", True, (250, 250, 250))
        inc = 0
        for i in range(15):
            self.Surface.blit(texto, (80,200 + inc))
            inc += 15
        
        
    def KeyEvent(self, key, event):
        if self.level == 0:
            if key[K_DOWN] == 1:
                self.selection = 1
            if key[K_UP] == 1:
                self.selection = 0
            if key[13] == 1:
                if self.selection == 0:
                    self.level = 1
                else:
                    self.level = -1
                    
        if self.level > 0:
            self.mybarr.move(pygame.mouse.get_pos()[0])
            if pygame.mouse.get_pressed()[0]==1:
                if self.myfires.__len__() < self.limfires:
                    self.laserSound.play()
                    self.myfires.append(Fire(pygame.mouse.get_pos()[0],445))
            if key[K_p] == 1:
                self.limfires = 100