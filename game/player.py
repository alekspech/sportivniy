import pygame
from varname.helpers import debug
import random
from game.game_settings import *
from game.bullet import Bullet

class PlayerKapibara(pygame.sprite.Sprite):
    def __init__(self, img_path, player_x, player_y):
        super().__init__()
        self.original_image = pygame.image.load(img_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50, 100))
        self.image = self.original_image
        self.flipped_image = pygame.transform.flip(self.original_image, flip_x=True, flip_y=False)
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y - self.rect.height
        self.hp = player_hp
        self.world_position = pygame.math.Vector2(player_x, player_y)

        self.jump_power = player_jump_power
        self.speed = pygame.math.Vector2(0,0)
        self.bullet_timer = weapon_timer
        self.is_facing_right = True
        self.is_on_ground = False


    def jump(self):
        if self.is_on_ground:
            self.speed.y = self.jump_power
            self.is_on_ground = False


    def shoot(self, dt, bullets_group, camera_offset):
        self.bullet_timer -= dt
        if self.bullet_timer <= 0:
            mouse_position = pygame.math.Vector2(
                pygame.mouse.get_pos()
            ) + camera_offset
            player_position = self.world_position + pygame.math.Vector2(self.rect.width//2, self.rect.height//2)
            shoot_direction = mouse_position - player_position
            shoot_direction = shoot_direction.normalize()
            bullets_group.add(
                Bullet(
                    img_path=bullet_img_path,
                    position=self.rect.center,
                    direction=shoot_direction
                )
            )# выстрел
            self.bullet_timer = weapon_timer

        

    def update(self, dt, bullets_group, walls_group, camera_offset):
        keys = pygame.key.get_pressed()
        movement = pygame.math.Vector2(0,0)

        if keys[pygame.K_a]:
            movement.x = -1
            self.flip_image(is_facing_left=True)
        if keys[pygame.K_d]:
            movement.x = 1
            self.flip_image(is_facing_left=False)
        if keys[pygame.K_SPACE]:
            self.jump()

        if movement.length() > 0:
            movement = movement.normalize()
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
        player_center_x = screen_position.x + self.rect.width//2



        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            if mouse_x < player_center_x:
                self.flip_image(is_facing_left=True)
            elif mouse_x > player_center_x:
                self.flip_image(is_facing_left=False)
            self.shoot(dt, bullets_group, camera_offset)

    def draw_hp(self, screen, camera_offset):
        hp_position = self.world_position - camera_offset
        hp_position.y -= int(self.rect.height * 3/4)      
        text_generator = pygame.font.SysFont('Comic Sans MS', size=20)
        text = text_generator.render(
            '{}'.format(self.hp), 1,(0,225,0)
        )
        screen.blit(text, dest = hp_position)

        # hp_position = self.rect.top

    def flip_image(self, is_facing_left ):
        if is_facing_left and self.is_facing_right:
            self.image = self.flipped_image
            self.is_facing_right = False
        elif not is_facing_left and not self.is_facing_right:
            self.image = self.original_image
            self.is_facing_right = True

    def  draw(self, screen, camera_offset):
        screen_position = self.world_position - camera_offset
        screen.blit(self.image, screen_position)
        