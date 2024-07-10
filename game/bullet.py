import pygame
from varname.helpers import debug
import random
from game.game_settings import screen_height, screen_width, gravity, bullet_speed

bullet_img = pygame.Surface((10,10))
bullet_img.fill((255,0,0))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        super().__init__()
        # self.image = pygame.image.load(img_path).convert_alpha()
        # self.image = pygame.transform.scale(self.image, (50, 100))
        self.image = bullet_img
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