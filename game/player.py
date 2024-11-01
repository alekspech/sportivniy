import pygame
from varname.helpers import debug
import random
from game.game_settings import *
from game.bullet import Bullet

class PlayerKapibara(pygame.sprite.Sprite):
    def __init__(self, img_path, player_x, player_y):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y - self.rect.height
        self.hp = player_hp

        self.jump_power = player_jump_power
        self.change_x = 0
        self.change_y = 0
        self.direction = pygame.math.Vector2(0,0)
        self.last_direction = pygame.math.Vector2(1,0)  #default right
        self.bullet_timer = weapon_timer

    def jump(self):
        if self.rect.y >= screen_height - self.rect.height: # проверка что игрок на полу
            self.change_y = self.jump_power
        return self.change_y

    def shoot(self, dt, bullets_group):
        self.bullet_timer -= dt
        if self.bullet_timer <= 0:
            mouse_position = pygame.math.Vector2(
                pygame.mouse.get_pos()
            )
            player_position = pygame.math.Vector2(self.rect.center)
            shoot_direction = mouse_position - player_position
            shoot_direction = shoot_direction.normalize()
            bullets_group.add(
                Bullet(
                    position=self.rect.center,
                    direction=shoot_direction
                )
            )# выстрел
            self.bullet_timer = weapon_timer

        

    def update(self, dt, bullets_group, walls_group):
        self.change_y += gravity
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.y >= screen_height - self.rect.height: # проверка что игрок на полу
            self.change_y = 0
            self.rect.y = screen_height - self.rect.height
        
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
            self.last_direction = self.direction
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0 #премешение игрока по иксу и по игрику
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1 
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += player_speed * dt
            self.direction.y = 1 
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= player_speed * dt
            self.direction.x = -1 
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += player_speed * dt
            self.direction.x = 1 
        if keys[pygame.K_SPACE]:
            self.jump()
        if keys[pygame.K_RETURN]:
            self.shoot(dt, bullets_group)  
        self.rect = self.rect.move(dx, dy)
        if pygame.sprite.spritecollideany(self, walls_group):
            self.rect = self.rect.move(-dx, -dy)

    def draw_hp(self, screen):
        hp_position = pygame.math.Vector2(self.rect.center)
        hp_position.y -= int(self.rect.height * 3/4)      
        text_generator = pygame.font.SysFont('Comic Sans MS', size=20)
        text = text_generator.render(
            '{}'.format(self.hp), 1,(0,225,0)
        )
        screen.blit(text, dest = hp_position)

        # hp_position = self.rect.top
