import pygame
import os 
from os import path
from data.settings import *

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, False, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
class Player(pygame.sprite.Sprite):
    def __init__(self, Game):
        pygame.sprite.Sprite.__init__(self)
        self.game = Game 
        self.image = pygame.transform.scale(self.game.player_img,(30, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 15
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 96
        self.time = 100
        self.score = 0
        self.speedx = 0
        self.speedy = 0
        self.onLogLeft = False
        self.onLogRight = False
        self.onLogFast = False
        self.life_count = 3
        self.last_update = pygame.time.get_ticks()

    def update(self):    
        now = pygame.time.get_ticks()
        if now - self.last_update > 2000:
            self.last_update = now 
            self.time = self.time - 5
            self.score = self.score + 10
        
        if self.onLogLeft:
            self.speedx = neg_logspeed
            self.speedy = 0
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            
        if self.onLogRight:
            self.speedx = pos_logspeed
            self.speedy = 0
            self.rect.x += self.speedx
            self.rect.y += self.speedy

        if self.onLogFast:
            self.speedx = fast_logspeed
            self.speedy = 0
            self.rect.x += self.speedx
            self.rect.y += self.speedy

    def draw_shield_bar(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 200
        BAR_HEIGHT = 15
        fill = (pct / 100) * BAR_LENGTH
        self.fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surf, GREEN, self.fill_rect)
        
class PlayerLife(pygame.sprite.Sprite):
    def __init__(self, Game, xvalue):
        pygame.sprite.Sprite.__init__(self)
        self.game = Game
        self.image = self.game.player_img
        self.rect = self.image.get_rect()
        self.rect.x = xvalue
        self.rect.bottom = 642
       
# Classes for Cars
class CarsLeft(pygame.sprite.Sprite):
    def __init__(self, Game, speed, spacing, start_x, bottom, width):
        pygame.sprite.Sprite.__init__(self)
        self.game = Game 
        self.image = self.game.car00_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 15
        self.rect.x = (start_x * (spacing + BOX_WIDTH))
        self.rect.bottom = bottom
        self.speedx = speed

    def update(self):       
        self.rect.x += self.speedx
        if self.rect.x < -30:
            self.rect.x = 480
        if self.rect.x > 480:
            self.rect.x = -30

class CarsRight(pygame.sprite.Sprite):
    def __init__(self, Game, speed, spacing, start_x, bottom, width):
        pygame.sprite.Sprite.__init__(self)
        self.game = Game 
        self.image = pygame.transform.rotate(self.game.car00_img, 180)
        self.rect = self.image.get_rect()
        self.radius = 15
        self.rect.x = (start_x * (spacing + BOX_WIDTH))
        self.rect.bottom = bottom
        self.speedx = speed

    def update(self):       
        self.rect.x += self.speedx
        if self.rect.x < -30:
            self.rect.x = 480
        if self.rect.x > 480:
            self.rect.x = -30

class TruckLeft(pygame.sprite.Sprite):
    def __init__(self, Game, speed, spacing, start_x, bottom, width):
        pygame.sprite.Sprite.__init__(self)
        self.game = Game
        self.image = self.game.truck_img
        self.rect = self.image.get_rect()
        self.rect.x = (start_x * (spacing + BOX_WIDTH))
        self.rect.bottom = bottom
        self.speedx = speed

    def update(self):       
        self.rect.x += self.speedx
        if self.rect.x < -30:
            self.rect.x = 480
        if self.rect.x > 480:
            self.rect.x = -30

class ShortLogs(pygame.sprite.Sprite):
    def __init__(self, Game, speed, spacing, start_x, bottom, width):
        pygame.sprite.Sprite.__init__(self)
        self.Game = Game
        self.image = self.Game.log_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = (start_x * (spacing + BOX_WIDTH))
        self.rect.bottom = bottom
        self.speedx = speed

    def update(self):
        self.rect.x += self.speedx
        if self.rect.x < -30:
            self.rect.x = 480
        if self.rect.x > 480:
            self.rect.x = -30

class LongLogs(pygame.sprite.Sprite):
    def __init__(self, Game, speed, spacing, start_x, bottom, width):
        pygame.sprite.Sprite.__init__(self)
        self.Game = Game
        self.image = pygame.transform.scale(self.Game.log_img, (LOG_WIDTH2, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = (start_x * (spacing + BOX_WIDTH))
        self.rect.bottom = bottom
        self.speedx = speed

    def update(self):
        self.rect.x += self.speedx
        if self.rect.x < -30:
            self.rect.x = 480
        if self.rect.x > 480:
            self.rect.x = -30         

class GrassObj(pygame.sprite.Sprite):
    def __init__(self, Game, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.game = Game
        self.image = self.game.end_img2  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class GrassObjTwo(pygame.sprite.Sprite):
    def __init__(self, Game, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.game = Game
        self.image = self.game.end_img  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class CenterWall(pygame.sprite.Sprite):
    def __init__(self, Game, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.game = Game
        self.image = self.game.center_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class EmptyObj(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class CapturedObj(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.transform.scale(self.game.saved_img,(width, height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
       
