import pygame
from varname.helpers import debug
import random

class NPC(pygame.sprite.Sprite):
    def __init__(self, img_path, player_x, player_y):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y - self.rect.height