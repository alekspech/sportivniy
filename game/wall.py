import pygame
from varname.helpers import debug
import random


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.world_position = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen, camera_offset):
        screen_position = self.world_position - camera_offset
        screen.blit(self.image, (screen_position.x, screen_position.y))