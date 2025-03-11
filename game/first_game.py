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

    player_group.update(dt, bullets_group, walls_group, camera_offset, npc_group)
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