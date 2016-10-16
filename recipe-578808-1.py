import pygame
from pygame.locals import *
import sys
import random
import os

pygame.init()

class Cell(pygame.sprite.Sprite):
    def __init__(self, game, pos, num):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.age=1
        self.game = game
        self.gen=0
        self.num = num
        self.color=self.getColor()
        self.parent = 0

        self.image = pygame.Surface([10,10])
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.alive = False
        self.edge = False

        self.a_neighbors = []
        self.d_neighbors = []

        self.n = (num - 74) - 1
        self.e = (num + 1) - 1
        self.s = (num + 74) - 1
        self.w = (num - 1) - 1
        self.ne = (self.n + 1)
        self.se = (self.s + 1)
        self.nw = (self.n - 1)
        self.sw = (self.s - 1)

        self.cell_list = [
            self.n,
            self.e,
            self.s,
            self.w,
            self.ne,
            self.se,
            self.nw,
            self.sw]

        self.game.cells.append(self)

    def getColor(self):
        if (self.age>0) and (self.age<=14):
            self.state="Child"
        elif (self.age>14) and (self.age<=60):
            self.state="Adult"
        elif (self.age>60) and (self.age<=100):
            self.state="Elder"
        if self.gen==0:
            if self.state=="Child":
                r,g,b=135,206,250
            elif self.state=="Adult":
                r,g,b=65,105,225
            elif self.state=="Elder":
                r,g,b=25,25,112
        elif self.gen==1:
            if self.state=="Child":
                r,g,b=255,182,193
            elif self.state=="Adult":
                r,g,b=255,20,147
            elif self.state=="Elder":
                r,g,b=176,48,96
        else:
            r,g,b=0,0,0
        return (r,g,b)
            
    def die(self):
        self.alive = False

    def survive(self):
        self.age+=1
        self.alive = True
        
    def born(self):
         self.alive=True
         self.gen=random.randint(0,1)
         
    def update(self):
        if not self.edge:
            self.a_neighbors = []
            self.d_neighbors = []
            neighbors = [self.game.cells[cell] for cell in self.cell_list]

            for n in neighbors:
                if n.alive:
                    self.a_neighbors.append(n)
                else:
                    self.d_neighbors.append(n)   

            if not self.game.running:
                    
                if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(self.game.mpos):
                    self.gen=0
                    self.alive = True
                    
                if pygame.mouse.get_pressed()[2] and self.rect.collidepoint(self.game.mpos):
                    self.gen=1
                    self.alive = True
                    
                if self.alive:
                    self.image.fill(self.getColor())
            else:
                if self.alive:
                    self.image.fill(self.getColor())
                    
                if not self.alive:
                    self.image.fill((0, 0, 0))
                    
        else:
            self.image.fill((255, 255, 255))
        

            


class Game():
    def __init__(self):
        #window setup
        pygame.display.set_caption('Game Of Life')
        
        # initiate the clock and screen
        self.gen=0
        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [740, 490]

        self.font = pygame.font.SysFont("Times New Roman", 19)

        self.sprites = pygame.sprite.Group()
        self.cells = []
        self.generation = 0
        self.population = 0
        self.gen=None
        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)

        self.running = False
        self.createGrid()
     
        while 1:
            self.Loop()

    def createGrid(self):
        col = 0
        row = 50
        cell_num = 0

        for y in xrange(44):
            for x in xrange(74):
                cell_num +=1
                cell = Cell(self, [col, row], cell_num)
                if row == 50 or row  == 480 or col == 0 or col == 730:
                    cell.edge = True
                self.sprites.add(cell)
                col += 10
            row += 10
            col = 0
          
    def Run(self):
        self.population = 0
        for cell in self.cells:
            if cell.alive:
                self.population += 1
                if (len(cell.a_neighbors) < 2) or (len(cell.a_neighbors)>3) or (cell.age==100):
                    cell.die()
                elif len(cell.a_neighbors) == 2 or len(cell.a_neighbors) == 3:
                    cell.survive()
            else:
                if (len(cell.a_neighbors) == 3):
                    d={i:[i.gen,i.state] for i in cell.a_neighbors}
                    if ([0,"Adult"] in d.values()) and ([1,"Adult"] in d.values()):
                        cell.born()
                    
    def blitDirections(self):
        text = self.font.render("Press Enter to begin, Space to pause and C to clear the board", 1, (255,255,255))
        generations = self.font.render("Generation: %s" %str(self.generation), 1, (255,255,255))
        pop = self.font.render("Pop: %s" %str(self.population), 1, (255,255,255))
        self.screen.blit(text, (10, 15))
        self.screen.blit(generations, (500, 15))
        self.screen.blit(pop, (650, 15))

    def Loop(self):
        # main game loop
        self.eventLoop()
        
        self.Tick()
        self.Draw()
        pygame.display.update()

    def eventLoop(self):
        # the main event loop, detects keypresses
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.running = True
                if event.key == K_SPACE:
                    self.running = False
                if event.key == K_c:
                    self.running=False
                    self.sprites.empty()
                    self.cells=[]
                    self.createGrid()
                    self.generation=0
                    self.population=0



    def Tick(self):
        # updates to player location and animation frame
        self.ttime = self.clock.tick()
        self.mpos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()
        if self.running:
            self.generation +=1
            self.Run()


    def Draw(self):
        self.screen.fill(0)
        self.blitDirections()
        self.sprites.update()
        self.sprites.draw(self.screen)

Game()
