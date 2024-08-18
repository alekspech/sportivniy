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
    player_x=screen_width-100,
    player_y=screen_height
)
npc_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
npc_group.add([player, npc1])
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
    
    npc_group.update(dt, bullets_group, walls_group)
    npc_group.draw(screen)
    walls_group.update()
    walls_group.draw(screen)
    bullets_group.update(dt)
    bullets_group.draw(screen)
    text = text_generator.render('{}'.format(player.rect.center), 1,(255,255,255))
    screen.blit(text, dest=player.rect.center)
    pygame.display.flip() #отрисовка обьектов 
    
pygame.quit()