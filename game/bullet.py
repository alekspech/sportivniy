import pygame
from varname.helpers import debug
import random
from game.game_settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, img_path, position, direction, damage):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        # self.image = pygame.transform.scale(self.image, (20, 25)) формат для молотова
        self.image = pygame.transform.scale(self.image, (7, 5))
        self.rect = self.image.get_rect()
        self.world_position = pygame.math.Vector2(position)
        self.speed = direction * bullet_speed
        self.damage = damage
        self.direction = direction
        
    def update(self, dt):
        self.world_position += self.speed * dt
        self.rect.center = self.world_position
        
    def draw(self, screen, camera_offset):
        right_vector = pygame.math.Vector2(1, 0)
        bullet_angle = -right_vector.angle_to(self.direction)
        rotated_img = pygame.transform.rotate(self.image, bullet_angle)
        screen_position = self.world_position - camera_offset
        screen.blit(rotated_img, screen_position)

class Bullets(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, screen, camera_offset):
        for sprite in self.sprites():
            sprite.draw(screen, camera_offset)