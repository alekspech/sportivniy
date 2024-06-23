import pygame
from varname.helpers import debug
import random


class PlayerKapibara(pygame.sprite.Sprite):
    def __init__(self, img_path, player_x, player_y, screen_h):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y - self.rect.height
        self.screen_h = screen_h
        self.gravity = 0.5
        self.jump_power = -10

        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.change_y += self.gravity # use gravity
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # check for ground collision
        if self.rect.y >= self.screen_h - self.rect.height:
            self.rect.y = self.screen_h - self.rect.height
            self.change_y = 0

    def jump(self):
        # unlimited jump
        self.change_y = self.jump_power
        # jump only on ground
        # if self.rect.y >= self.screen_h - self.rect.height:
        #     self.change_y = self.jump_power
        
