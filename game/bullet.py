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
        self.world_position = pygame.math.Vector2(position)
        self.speed = direction * bullet_speed
        self.damage = 10
        print('bullet created')

    def update(self, dt):
        self.world_position += self.speed * dt
        self.rect.center = self.world_position
        # if self.rect.bottom < 0:
        #     self.kill()
        # if self.rect.top > screen_height:
        #     self.kill()
        # if self.rect.left < 0:
        #     self.kill()
        # if self.rect.right > screen_width:
        #     self.kill()
        
        if self.world_position.y < -100 or self.world_position.y > 10000:
            self.kill()
        if self.world_position.x < -1000 or self.world_position.x > 10000:
            self.kill()

    def draw(self, screen, camera_offset):
        screen_position = self.world_position - camera_offset
        screen.blit(self.image, (screen_position.x, screen_position.y))