import pygame
from varname.helpers import debug
import random
from game.game_settings import *
from game.bullet import Bullet

class Weapon(pygame.sprite.Sprite):
    def __init__(self, weapon_name, damage, fire_rate, img_path):
        super().__init__()
        self.original_image = pygame.image.load(img_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50, 30))
        self.image = self.original_image
        self.flipped_image = pygame.transform.flip(self.original_image, flip_x=True, flip_y=False)
        self.rect = self.image.get_rect()
        self.damage = damage
        self.fire_rate = fire_rate
        self.weapon_name = weapon_name
        self.bullet_timer = self.fire_rate
    
    def draw(self, screen, camera_offset, player):
        screen_position = player.world_position - camera_offset + pygame.math.Vector2(player.rect.width // 2, player.rect.height // 2)
        screen.blit(self.image, screen_position)

class RangedWeapon(Weapon):
    def __init__(self, weapon_name, bullets_count, damage, fire_rate, img_path):
        super().__init__(weapon_name, damage, fire_rate, img_path)
        self.bullets_count = bullets_count
        
    def shoot(self,dt, bullets_group, camera_offset, player):
        self.bullet_timer -= dt
        if self.bullet_timer <= 0:
            mouse_position = pygame.math.Vector2(
                pygame.mouse.get_pos()
            ) + camera_offset
            player_position = player.world_position + pygame.math.Vector2(player.rect.width//2, player.rect.height//2)
            shoot_direction = mouse_position - player_position
            shoot_direction = shoot_direction.normalize()
            bullets_group.add(
                Bullet(
                    img_path=bullet_img_path,
                    position=player.rect.center,
                    direction=shoot_direction
                )
            )# выстрел
            self.bullet_timer = weapon_timer
        

class MeleeWeapon(Weapon):
    def __init__(self, weapon_name, attack_range, damage, fire_rate, img_path):
        super().__init__(weapon_name, damage, fire_rate, img_path)
        self.attack_range = attack_range

    def shoot(self,dt, bullets_group, camera_offset, player):
        return
    
class ThrowingWeapon(Weapon): 
    def __init__(self, weapon_name, bullets_count, damage, fire_rate, img_path, attack_range, flash_time):
        super().__init__(weapon_name, damage, fire_rate, img_path)
        self.bullets_count = bullets_count
        self.attack_range = attack_range
        self.flash_time = flash_time