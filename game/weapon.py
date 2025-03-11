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
        self.flipped_image = pygame.transform.flip(self.original_image, flip_x=True, flip_y=False)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.damage = damage
        self.fire_rate = fire_rate
        self.weapon_name = weapon_name

    def draw(self, screen, player, camera_offset):
        """Draws the weapon attached to the player and rotates it toward the mouse"""
        mouse_pos = pygame.mouse.get_pos()
        player_screen_pos = player.world_position - camera_offset + pygame.math.Vector2(player.rect.width // 2, player.rect.height // 2)

        # Calculate angle to rotate weapon
        angle_m = -1
        if mouse_pos[0] < player_screen_pos.x:
            angle_m = 1
            self.image = self.flipped_image
        else:
            self.image = self.original_image
        angle = angle_m * (mouse_pos - player_screen_pos).angle_to(pygame.math.Vector2(1, 0))

        # Rotate image
        self.image = pygame.transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect(center=player_screen_pos)

        # Draw on screen
        screen.blit(self.image, self.rect.topleft)

class RangedWeapon(Weapon):
    def __init__(self, weapon_name, bullets_count, damage, fire_rate, img_path):
        super().__init__(weapon_name, damage, fire_rate, img_path)
        self.bullets_count = bullets_count
        self.bullet_timer = self.fire_rate
        
    def shoot(self, dt, player, bullets_group, camera_offset):
        self.bullet_timer -= dt
        if self.bullet_timer <= 0:
            mouse_position = pygame.math.Vector2(
                pygame.mouse.get_pos()
            ) + camera_offset
            player_position = player.world_position + pygame.math.Vector2(
                player.rect.width//2, 
                player.rect.height//2
            )
            shoot_direction = mouse_position - player_position
            shoot_direction = shoot_direction.normalize()
            bullets_group.add(
                Bullet(
                    img_path=bullet_img_path,
                    position=player.rect.center,
                    direction=shoot_direction
                )
            )# выстрел
            self.bullet_timer = self.fire_rate
        

class MeleeWeapon(Weapon):
    def __init__(self, weapon_name, attack_range, damage, fire_rate, img_path):
        super().__init__(weapon_name, damage, fire_rate, img_path)
        self.attack_range = attack_range
        self.attack_timer = self.fire_rate

    def attack(self, dt, player, npc_group):
        self.attack_timer -= dt
        if self.attack_timer <= 0:
            for npc in npc_group:
                distance = player.world_position.distance_to(npc.world_position)
                if distance <= self.attack_range:
                    npc.hp -= self.damage
                    if npc.hp <= 0:
                        npc_group.remove(npc)
            self.bullet_timer = self.fire_rate


class ThrowingWeapon(Weapon): 
     def __init__(self, weapon_name, bullets_count, damage, fire_rate, img_path):
         super().__init__(weapon_name, damage, fire_rate, img_path)
         self.bullets_count = bullets_count