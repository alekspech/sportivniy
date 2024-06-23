import pygame
from varname.helpers import debug
import random
from game.game_settings import screen_height, screen_width, gravity

class PlayerKapibara(pygame.sprite.Sprite):
    def __init__(self, img_path, player_x, player_y):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y - self.rect.height

        self.jump_power = -10
        self.change_x = 0
        self.change_y = 0

    def jump(self):
        if self.rect.y >= screen_height - self.rect.height: # проверка что игрок на полу
            self.change_y = self.jump_power

    def update(self):
        self.change_y += gravity
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.y >= screen_height - self.rect.height: # проверка что игрок на полу
            self.change_y = 0
            self.rect.y = screen_height - self.rect.height