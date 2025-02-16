import pygame
from varname.helpers import debug
import random
from game.game_settings import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, img_path, spawn_x, spawn_y, player):
        super().__init__()
        self.original_image = pygame.image.load(img_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50, 100))
        self.image = self.original_image
        self.flipped_image = pygame.transform.flip(self.original_image, flip_x=True, flip_y=False)
        self.rect = self.image.get_rect()
        self.rect.x = spawn_x
        self.rect.y = spawn_y - self.rect.height
        # self.change_x = 0
        # self.change_y = 0
        self.hp = npc_hp
        self.npc_speed = npc_speed
        self.world_position = pygame.math.Vector2(spawn_x, spawn_y)
        self.player = player #ссылка на игрока
        self.attack_timer = npc_attack_timer_melee
        self.jump_power = player_jump_power
        self.speed = pygame.math.Vector2(0,0)
        self.bullet_timer = weapon_timer
        self.is_facing_right = True
        self.is_on_ground = False

    def collide_bullet(self, bullets_group):
        bullet = pygame.sprite.spritecollideany(self, bullets_group)
        if bullet is not None:
            bullets_group.remove(bullet)
            self.hp -= weapon_attack
            if self.hp < 0:
                self.hp = 0
            self.npc_speed -= weapon_attack
            if self.npc_speed < 0:
                self.npc_speed = 0
            if self.hp <= 0:
                self.npc_speed = 0

    def update(self, dt, bullets_group, walls_group, camera_offset):
        movement = pygame.math.Vector2(0, 0)

        player_position = pygame.math.Vector2(self.player.rect.center)
        npc_position = pygame.math.Vector2(self.rect.center)
        direction = player_position - npc_position
        distance_to_player = direction.length()
        if distance_to_player > 0:
            direction = direction.normalize()

        if distance_to_player > npc_attack_range:
            movement = direction * self.npc_speed * dt
            self.rect.x += movement.x
            self.rect.y += movement.y
        else:
            self.attack(dt)
        self.collide_bullet(bullets_group)
        if movement.length() > 0:
            movement = movement.normalize()
        if movement.x < 0:
            self.flip_image(is_facing_left = True)
        if movement.x > 0:
            self.flip_image(is_facing_left = False)    

        self.world_position.x += movement.x * player_speed * dt
        self.rect.topleft = self.world_position
        collided_object = pygame.sprite.spritecollideany(self, walls_group)
        #пересечение со стеной, движение по горизонтали
        if collided_object:
            if movement.x > 0:
                self.world_position.x = collided_object.rect.left - self.rect.width
            elif movement.x < 0:
                self.world_position.x = collided_object.rect.right
            self.rect.topleft = self.world_position
        
        #пересечение со стеной, движение по вертикали
        self.speed.y += gravity
        self.world_position.y += self.speed.y
        self.rect.topleft = self.world_position
        collided_object = pygame.sprite.spritecollideany(self, walls_group)
        if collided_object:  #есть пересечение   
            if self.speed.y > 0: #игрок падает на объект 
                self.is_on_ground = True
                self.speed.y = 0
                self.world_position.y = collided_object.rect.top - self.rect.height
            elif self.speed.y < 0: #игрок прыгает
                self.speed.y = 0
        else:
            self.is_on_ground = False
        self.rect.topleft = self.world_position
        screen_position = self.world_position - camera_offset

    def draw_hp(self, screen, camera_offset):
        hp_position = self.world_position - camera_offset
        hp_position.y -= int(self.rect.height * 3/4)      
        text_generator = pygame.font.SysFont('Comic Sans MS', size=20)
        text = text_generator.render(
            '{}'.format(self.hp), 1,(255,0,0)
        )
        screen.blit(text, dest = hp_position)

    def attack(self, dt):
        self.attack_timer -= dt
        if self.attack_timer <= 0:
            self.player.hp -= npc_weapon_attack_melee
            self.attack_timer = npc_attack_timer_melee

    def  draw(self, screen, camera_offset):
        screen_position = self.world_position - camera_offset
        screen.blit(self.image, screen_position)

    def flip_image(self, is_facing_left ):
        if is_facing_left and self.is_facing_right:
            self.image = self.flipped_image
            self.is_facing_right = False
        elif not is_facing_left and not self.is_facing_right:
            self.image = self.original_image
            self.is_facing_right = True   
        