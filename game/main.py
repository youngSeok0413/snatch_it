"""snatch game
    how to make game using pygame!!
"""
import pygame
import random

pygame.init()

RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Player:
    def __init__(self, win, x, y, width, height):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.grab = False
        self.grabCount = 0

        self.hold = False

        # self.animation = [] #here animation(grapb) spread -> hold

    def draw(self):
        if self.grabCount + 1 > 2:
            self.grabCount = 2
        elif self.grabCount - 1 < 0:
            self.grabCount = 0

        if self.grab:
            # win.blit(self.animation[self.grabCount], (self.x, self.y))
            pygame.draw.rect(self.win, (0, 255, 0),
                             (self.x, self.y, self.width, self.height))
            self.grabCount += 1
        else:
            # win.blit(self.animation[self.grabCount], (self.x, self.y))
            pygame.draw.rect(self.win, (255, 255, 0),
                             (self.x, self.y, self.width, self.height))
            self.grabCount -= 1


class Stick:
    def __init__(self, win, color, x, y, a, width, height):
        self.win = win
        self.color = color
        self.x = x
        self.y = y
        self.a = a
        self.width = width
        self.height = height
        self.time = 0
        self.color = color
        # self.image = pygame.image.load()#here stick image

    def falling(self):
        self.time += 1/60
        print("falling : ", self.time, ", ", self.y)
        self.y = 0.5*self.a*self.time*self.time
        
    def collide(self, y1, height):
        if self.y+self.height > y1 and self.y+self.height < y1+height:
            return True
        elif self.y > y1 and self.y < y1+height:
            return True
        
        return False
    
    def draw(self):
        pygame.draw.rect(self.win, self.color,
                         (self.x, self.y, self.width, self.height))


class Game:
    def __init__(self, width, height, frame):
        self.width = width
        self.height = height
        
        self.frame = frame
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.SysFont(None, 30)
        
        self.running = True
        self.gameover = False
        
        self.score = 0
        self.level = 1
        
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption("SNATCH IT!!")

        self.player = Player(self.win, 200, 400, 100, 80)
        self.sticks = []

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:  # need to change(usart)
                if event.key == pygame.K_r:
                    self.gameover = False
                    self.score = 0
                    self.level = 1
                    #reset the game
                    
            #if event.type == pygame.KEYDOWN:  # need to change(usart)
            #    if event.key == pygame.K_SPACE:
            #        self.player.grab = not self.player.grab
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] :
                self.player.grab = True           
            else:
                self.player.grab = False

        if(self.gameover) :
            return
        
        #stick gen+del
        if self.sticks:
            print("num:"+str(len(self.sticks)))
            for stick in self.sticks:
                
                rem = False
                
                #player-stick
                if stick.collide(self.player.y, self.player.height):
                    if self.player.grab:
                        if stick.color == RED:
                            self.score += 10
                            rem = True
                        if stick.color == BLUE:
                            self.gameover = True
                            rem = True    
                #floor-stick
                if stick.collide(self.height, 1000):
                    if stick.color == RED:
                        self.gameover = True
                        rem = True
                    if stick.color == BLUE:
                        self.score += 10
                        rem = True    
                
                if(rem):
                    self.sticks.remove(stick)
                else:
                    stick.falling()
        else:
            self.newStick()
            

    def newStick(self):
        color = random.randrange(0, 2)
        print("color:",color)
        if color == 0:
            self.sticks.append(Stick(self.win, RED, 245, 0, 400 + 10*self.level, 10, 80))
        if color == 1:
            self.sticks.append(Stick(self.win, BLUE, 245, 0, 400 + 10*self.level, 10, 80))
        self.level += 10
        
    def render(self):
        self.win.fill((0, 0, 0))
        
        if self.gameover:
            gameover = self.font.render("Game Over", True, (255,255,255))
            self.win.blit(gameover, (self.width/2-100, self.height/2-60))
            score = self.font.render("SCORE:" + str(self.score) + ", press R to restart", True, (255,255,255)) 
            self.win.blit(score, (self.width/2-100, self.height/2-29))
        else :
            score = self.font.render("SCORE:" + str(self.score), True, (255,255,255)) 
            self.win.blit(score, (350,10)) 
            self.player.draw()
            for stick in self.sticks:
                stick.draw()

        pygame.display.update()

    def run(self):
        while (self.running):
            self.clock.tick(self.frame)

            self.update()
            self.render()


game = Game(500, 570, 60)

game.run()
