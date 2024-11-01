import pygame
from varname.helpers import debug
import random
from game.game_settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, img_path, position, direction):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (7, 5))
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(position)
        self.speed = direction * bullet_speed
        self.damage = 10

    def update(self, dt):
        self.position += self.speed * dt
        self.rect.center = self.position
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > screen_height:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > screen_width:
            self.kill()