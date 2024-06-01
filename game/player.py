import pygame
from varname.helpers import debug
import random

class PlayerKapibara(pygame.sprite.Sprite):
    def __init__(self, img_path):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (100,100)