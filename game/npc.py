import pygame
from varname.helpers import debug
import random
from game.game_settings import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, img_path, spawn_x, spawn_y, player):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x = spawn_x
        self.rect.y = spawn_y - self.rect.height
        self.change_x = 0
        self.change_y = 0
        self.hp = npc_hp
        self.speed = npc_speed
        self.player = player #ссылка на игрока

    def update(self, dt, bullets_group, walls_group):
        self.change_y += gravity
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.y >= screen_height - self.rect.height: # проверка что игрок на полу
            self.change_y = 0
            self.rect.y = screen_height - self.rect.height

        player_position = pygame.math.Vector2(self.player.rect.center)
        npc_position = pygame.math.Vector2(self.rect.center)
        direction = player_position - npc_position
        distance_to_player = direction.length()
        if distance_to_player > 0:
            direction = direction.normalize()

        if distance_to_player > npc_attack_range:
            movement = direction * self.speed * dt
            self.rect.x += movement.x
            self.rect.y += movement.y
        
        bullet = pygame.sprite.spritecollideany(self, bullets_group)
        if bullet is not None:
            bullets_group.remove(bullet)
            self.hp -= weapon_attack
            if self.hp < 0:
                self.hp = 0
            self.speed -= weapon_attack
            if self.speed < 0:
                self.speed = 0
            if self.hp <= 0:
                self.speed = 0

    def draw_hp(self, screen):
        # hp_position = pygame.math.Vector2(self.rect.topleft)
        hp_position = pygame.math.Vector2(self.rect.center)
        hp_position.y -= int(self.rect.height * 3/4)      
        text_generator = pygame.font.SysFont('Comic Sans MS', size=20)
        text = text_generator.render(
            '{}'.format(self.hp), 1,(255,0,0)
        )
        screen.blit(text, dest = hp_position)
   
