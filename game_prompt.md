Update the context to use pygame to help 14 year old teenager learn programming and Python3. The game is side view 2D shooter where global coordinates and gravity are already implemented.

We currently have following code, remember and understand the project structure to answer questions later

import pygame
from varname.helpers import debug
import random
from game.game_settings import *
from game.bullet import Bullet
from game.game_tools import round_vector

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
        

import pygame
from varname.helpers import debug
import random
from game.game_settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, img_path, position, direction):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (7, 5))
        self.rect = self.image.get_rect()
        self.world_position = pygame.math.Vector2(position)
        self.speed = direction * bullet_speed
        self.damage = 10

    def update(self, dt):
        self.world_position += self.speed * dt
        self.rect.center = self.world_position
        # if self.rect.bottom < 0:
        #     self.kill()
        # if self.rect.top > screen_height:
        #     self.kill()
        # if self.rect.left < 0:
        #     self.kill()
        # if self.rect.right > screen_width:
        #     self.kill()
        
    def draw(self, screen, camera_offset):
        screen_position = self.world_position - camera_offset
        screen.blit(self.image, screen_position)


import pygame
from varname.helpers import debug
import random
from game.game_settings import *
from game.game_tools import round_vector

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
        

# game/game_settings.py

screen_height = 800
screen_width = 1280
gravity = 0.5
bullet_speed = 1000
is_fullscreen = True
player_speed = 300
npc_speed = 250
weapon_timer = 0.2
player_jump_power = -10
bg_path = 'textures/background.JPG'
player_img_path = 'textures/kapibara.png'
npc1_img_path = 'textures/NPC1.png'
bullet_img_path = 'textures/bullet.png'
npc2_img_path = 'textures/NPC2.png'
bullet_img_path2 = 'textures/bullet2.jpg'
grenade_img_path = 'textures/Granade.png'
knife_img_path = 'textures/knife.png'
gun_img_path = 'textures/Gun.png'
npc_attack_range = 30
npc_attack_timer_melee = 1
npc_hp = 100
npc_spawn_timer = 1.5
weapon_attack = 30
npc_weapon_attack_melee = 10
player_hp = 100
world_cell_size = 32

# game/first_game.py

import pygame
import os
from varname.helpers import debug
import random
from game.player import PlayerKapibara
from game.bullet import Bullet
from game.wall import Wall
from game.npc import NPC
from game.game_settings import *

log_path = 'log/log.txt'
os.makedirs('log', exist_ok=True)
log_file = open(log_path, 'w')
print(log_path)
pygame.init()
if is_fullscreen:
    screen = pygame.display.set_mode(
        (screen_width,screen_height),
        pygame.FULLSCREEN | pygame.SCALED
    )   
else:
    screen = pygame.display.set_mode((screen_width,screen_height))  
clock = pygame.time.Clock()
is_game_running = True
dt = 0
text_generator = pygame.font.SysFont('Comic Sans MS', size=30)
bg = pygame.image.load(bg_path)
bg = pygame.transform.scale(bg, (screen_width, screen_height))
player = PlayerKapibara(
    img_path=player_img_path,
    player_x=0,
    player_y=0
)
npc1 = NPC(
    img_path=npc1_img_path,
    spawn_x=screen_width-100,
    spawn_y=screen_height,
    player=player
)
npc2 = NPC(
    img_path=npc2_img_path,
    spawn_x=screen_width-50,
    spawn_y=screen_height,
    player=player
)
npc_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()

player_group.add([player])
walls_group.add(
    [
        Wall(x=0, y=0, width=10000, height=10, color='black' ),
        Wall(x=-200, y=0, width=100, height=10, color='yellow' ),
        Wall(x=-400, y=0 ,width=100, height=10, color='green' ),
        Wall(x=-400, y=-100, width=10, height=100, color='green' ),
    ]
)
game_frame_number = 0 
last_npc_spawn_time = 0
while is_game_running: # основной цикл игры
    dt = clock.tick(60) / 1000
    game_frame_number += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game_running = False

    bg_h = screen.get_height()-bg.get_height()
    bg_w = screen.get_width()-bg.get_width()
    screen.blit(bg, (bg_w, bg_h))
    camera_offset = player.world_position - pygame.math.Vector2(
        screen_width/2,
        screen_height*3/4
    )


    
    
    player_position_screen = player.world_position - camera_offset

    player_group.update(dt, bullets_group, walls_group, camera_offset)
    npc_group.update(dt, bullets_group, walls_group, camera_offset)
    for npc in npc_group:
        npc.draw(screen, camera_offset)
        npc.draw_hp(screen, camera_offset)
        if npc.hp <= 0:
            npc_group.remove(npc)
    for player in player_group:
        player.draw_hp(screen, camera_offset)
        player.draw(screen, camera_offset)

        if player.hp <= 0:
            exit()
    walls_group.update()
    # walls_group.draw(screen)
    for wall in walls_group:
        wall.draw(screen, camera_offset)
    bullets_group.update(dt)
    # bullets_group.draw(screen)
    for bullet in bullets_group:
        bullet.draw(screen, camera_offset)
    player_position_str = 'player: {}'.format(player.world_position)
    text = text_generator.render(
        player_position_str, 1,(0,0,0)
        )
    screen.blit(text, dest=(0,0))
    game_time = pygame.time.get_ticks()
    game_time_str = 'game time: {}'.format(game_time)
    text = text_generator.render(
        game_time_str,
        1,
        (0,255,0)
    )
    screen.blit(text, dest=(0,30))
    player_speed_str = 'player speed: {}'.format(player.speed)
    text = text_generator.render(
        player_speed_str,
        1,
        (255,0,0)
    )
    screen.blit(text, dest=(0,60))
    log_file.write(game_time_str + ', ')
    log_file.write(player_position_str + ', ')
    log_file.write(player_speed_str + '\n')
    pygame.display.flip() #отрисовка обьектов
    if game_time - last_npc_spawn_time > npc_spawn_timer * 1000:
        new_npc = NPC(
            img_path=npc1_img_path,
            spawn_x=player.rect.x + random.randint(300, 1000),
            spawn_y=player.rect.y,
            player=player
        )

        npc_group.add(new_npc)
        npc_spawn_x = player.rect.x + random.randint(300, 1000)
        last_npc_spawn_time = game_time
    
pygame.quit()
log_file.close()