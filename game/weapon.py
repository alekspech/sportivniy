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
        if player.is_facing_right == True:
            screen_position = player.world_position - camera_offset + pygame.math.Vector2(player.rect.width // 2, player.rect.height // 2)
            screen.blit(self.image, screen_position)
        elif player.is_facing_right == False:
            screen_position = player.world_position - camera_offset + pygame.math.Vector2(-player.rect.width // 2, player.rect.height // 2)
            screen.blit(self.flipped_image, screen_position)

class RangedWeapon(Weapon):
    def __init__(self, weapon_name, bullets_count, damage, fire_rate, img_path, reload_time):
        super().__init__(weapon_name, damage, fire_rate, img_path)
        self.bullets_count = bullets_count #сейчас патронов в обойме
        self.max_bullets_count = bullets_count#патронов в обойме
        self.reload_time = reload_time
        self.reload_timer = 0
        self.reloading = False

    def reload(self):
        self.reloading = True
        self.reload_timer = self.reload_time
    
    def update_reload(self,dt):
        if self.reloading:
            self.reload_timer -= dt
            if self.reload_timer <= 0:
                self.bullets_count = self.max_bullets_count
                self.reloading = False

    def shoot(self,dt, bullets_group, camera_offset, player):
        self.bullet_timer -= dt
        if self.bullet_timer <= 0:
            mouse_position = pygame.math.Vector2(
                pygame.mouse.get_pos()
            ) + camera_offset
            player_position = player.world_position + pygame.math.Vector2(player.rect.width//2, player.rect.height//2)
            shoot_direction = mouse_position - player_position
            shoot_direction = shoot_direction.normalize()
            bullet_position = player_position + pygame.math.Vector2(
                self.image.get_width()*3//4,
                self.image.get_height()//2
            )
            if player.is_facing_right == False:
                bullet_position = player_position + pygame.math.Vector2(
                    -self.image.get_width()*3//4,
                    self.image.get_height()//2
                )
            if self.weapon_name == 'gun':
                bullet_img = gun_bullet_img_path
            elif self.weapon_name == 'machine gun':
                bullet_img = machine_gun_bullet_img_path   
            bullets_group.add(
                Bullet(
                    img_path=bullet_img,
                    position=bullet_position,
                    direction=shoot_direction,
                    damage=self.damage
                )
            )# выстрел
            self.bullet_timer = self.fire_rate
        

class MeleeWeapon(Weapon):
    def __init__(self, weapon_name, attack_range, damage, fire_rate, img_path):
        super().__init__(weapon_name, damage, fire_rate, img_path)
        self.attack_range = attack_range

    def attack(self, dt, player, npc_group):
        self.bullet_timer -= dt
        if self.bullet_timer <= 0:
            for npc in npc_group:
                direction = npc.world_position.x - player.world_position.x
                distance = player.world_position.distance_to(npc.world_position)
                if distance <= self.attack_range:
                    if direction < 0 and player.is_facing_right == False:
                        npc.hp -= self.damage
                    if direction > 0 and player.is_facing_right:
                        npc.hp -= self.damage
    
class ThrowingWeapon(Weapon): 
    def __init__(self, weapon_name, bullets_count, damage, fire_rate, img_path, attack_range, flash_time):
        super().__init__(weapon_name, damage, fire_rate, img_path)
        self.bullets_count = bullets_count
        self.attack_range = attack_range
        self.flash_time = flash_time