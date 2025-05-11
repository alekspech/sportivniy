import pygame
from varname.helpers import debug
import random
from game.game_settings import *
from game.bullet import Bullet
from game.game_tools import round_vector
from game.weapon import RangedWeapon, MeleeWeapon, ThrowingWeapon

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
        self.is_facing_right = True
        self.is_on_ground = False
        self.arsenal = {
            3: MeleeWeapon(
                'knife',
                attack_range=knife_attack_range, 
                damage=knife_damage, 
                fire_rate=knife_fire_rate, 
                img_path=knife_img_path
            ),
            2: RangedWeapon(
                'gun', 
                bullets_count=gun_bullets_count, 
                damage=gun_damage, 
                fire_rate=gun_fire_rate, 
                img_path=gun_img_path,
                reload_time=1
            ),
            1: RangedWeapon(
                'machine gun', 
                bullets_count=machine_gun_bullets_count, 
                damage=machine_gun_damage, 
                fire_rate=machine_gun_fire_rate, 
                img_path=machine_gun_img_path,
                reload_time=2
            ),
            4: ThrowingWeapon(
                'flash grenade',
                bullets_count = grenade_bullets_count,
                flash_time=flash_time,
                attack_range=flash_attack_range,
                img_path=flash_img_path,
                damage=flash_damage,
                fire_rate=grenade_fire_rate
            )
        }
        self.current_weapon = 1

    def jump(self):
        if self.is_on_ground:
            self.speed.y = self.jump_power
            self.is_on_ground = False

    def update(self, dt, bullets_group, walls_group, camera_offset, npc_group):
        keys = pygame.key.get_pressed()
        for i in range(0,9):
            if keys[getattr(pygame, f'K_{i}')]:
                if i in self.arsenal:
                    self.current_weapon = i

        weapon = self.arsenal[self.current_weapon]
        if isinstance(weapon, RangedWeapon):
            weapon.update_reload(dt)
        movement = pygame.math.Vector2(0,0)

        if keys[pygame.K_a]:
            movement.x = -1
            self.flip_image(is_facing_left=True)
        if keys[pygame.K_d]:
            movement.x = 1
            self.flip_image(is_facing_left=False)
        if keys[pygame.K_SPACE]:
            self.jump()
        if keys[pygame.K_r]:
            if isinstance(weapon, RangedWeapon):
                weapon.reload()

        if movement.length() > 0:
            movement = movement.normalize()
        self.world_position.x += movement.x * player_speed * dt
        self.world_position = round_vector(self.world_position)
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
        self.world_position = round_vector(self.world_position)
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
        self.world_position = round_vector(self.world_position)
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
            if isinstance(weapon, RangedWeapon):
                weapon.shoot(dt, bullets_group, camera_offset, self)
            elif isinstance(weapon, MeleeWeapon):
                weapon.attack(dt, self, npc_group)

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

    def draw(self, screen, camera_offset):
        screen_position = self.world_position - camera_offset
        screen.blit(self.image, screen_position)
        self.arsenal[self.current_weapon].draw(screen, camera_offset, self)
    
    def draw_ammo(self, screen):
        weapon = self.arsenal[self.current_weapon]
        if not isinstance(weapon, RangedWeapon):
            return
        text_color = (255,255,255)
        bar_bg_color = (50,50,50)
        bar_fg_color = (52,42,200)
        text_generator = pygame.font.SysFont('Comic Sans MS', size=30)
        ammo_text = f'{weapon.bullets_count} / {weapon.max_bullets_count}'
        text_render = text_generator.render(ammo_text,True, text_color)
        text_rect = text_render.get_rect()
        text_rect.bottomleft = (screen.get_width()-10-text_rect.width,screen.get_height()-10)
        screen.blit(text_render, text_rect)

        if weapon.reloading:
            bar_width = 100
            bar_height = 10
            bar_x = 50
            bar_y = text_rect.top - 20
            reload_progress = 1 - (weapon.reload_timer / weapon.reload_time)

            pygame.draw.rect(
                screen, 
                bar_bg_color, 
                (
                    bar_x, 
                    bar_y, 
                    bar_width, 
                    bar_height
                )
            )
            pygame.draw.rect(
                screen, 
                bar_fg_color, 
                (
                    bar_x, 
                    bar_y, 
                    int(bar_width * reload_progress), 
                    bar_height
                )
            )