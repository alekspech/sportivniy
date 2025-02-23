import pygame
from varname.helpers import debug
import random
from game.game_settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self, weapon_name, damage, fire_rate, img_path):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.damage = damage
        self.fire_rate = fire_rate
        self.weapon_name = weapon_name

class RangedWeapon(Weapon):
    def __init__(self, weapon_name, bullets_count, damage, fire_rate, img_path):
        super().__init__(weapon_name, damage, fire_rate, img_path)
        self.bullets_count = bullets_count
        
    # def shoot(self,dt, player, bullets_group, camera_offset):
        
        

class MeleeWeapon(Weapon):
    def __init__(self, weapon_name, attack_range, damage, fire_rate, img_path):
        super().__init__(weapon_name, damage, fire_rate, img_path)
        self.attack_range = attack_range
