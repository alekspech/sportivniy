import pygame
from varname.helpers import debug
import random
from game.player import PlayerKapibara
from game.bullet import Bullet
from game.wall import Wall
from game.npc import NPC
from game.game_settings import *

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
    player_y=screen_height
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
npc_group.add([npc1, npc2])
player_group.add([player])
walls_group.add(
    [
        Wall(x=-1,y=-2,width=10000,height=2,color='black' ),
        Wall(x=1,y=screen_height+1,width=10000,height=2,color='black' ),
        Wall(x=-1,y=1,width=2,height=10000,color='black' ),
        Wall(x=screen_width+1,y=1,width=2,height=10000,color='black' ),
    ]
)
game_frame_number = 0
heals = []
while is_game_running: # основной цикл игры
    dt = clock.tick(60) / 1000
    game_frame_number += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game_running = False

    bg_h = screen.get_height()-bg.get_height()
    bg_w = screen.get_width()-bg.get_width()
    screen.blit(bg, (bg_w, bg_h))
    
    player_group.update(dt, bullets_group, walls_group)
    player_group.draw(screen)
    npc_group.update(dt, bullets_group, walls_group)
    npc_group.draw(screen)
    for npc in npc_group:
        npc.draw_hp(screen)
        if npc.hp == 0:
            npc_group.remove(npc)
    walls_group.update()
    walls_group.draw(screen)
    bullets_group.update(dt)
    bullets_group.draw(screen)
    text = text_generator.render('{}'.format(player.rect.center), 1,(255,255,255))
    screen.blit(text, dest=(0,0))
    pygame.display.flip() #отрисовка обьектов
    # game_time = round(pygame.time.get_ticks()/1000)
    # if game_time % 2 == 0:
        # new_npc = NPC(
        #     img_path=npc1_img_path,
        #     spawn_x=screen_width-100,
        #     spawn_y=screen_height,
        #     player=player
        # )
        # npc_group.add(new_npc)
    # print(game_time)
    
pygame.quit()
