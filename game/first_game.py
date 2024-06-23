import pygame
from varname.helpers import debug
import random
from game.player import PlayerKapibara
from game.wall import Wall
from game.npc import NPC
from game.game_settings import screen_height, screen_width

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))   
# screen_width = screen.get_width()
# screen_height = screen.get_height()
clock = pygame.time.Clock()
is_game_running = True
dt = 0
player_speed = 200
player_img_path = 'textures/kapibara.jpeg'
npc1_img_path = 'textures/NPC1.jpeg'
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
    game_frame_number += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game_running = False

    screen.fill('blue')
    mouse_position = pygame.mouse.get_pos()
    player_color = 'green'

    keys = pygame.key.get_pressed()
    dx = 0
    dy = 0 #премешение игрока по иксу и по игрику
    # if keys[pygame.K_w] or keys[pygame.K_UP]:
    #     dy -= player_speed * dt 
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dy += player_speed * dt
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        dx -= player_speed * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        dx += player_speed * dt
    if keys[pygame.K_SPACE]:
        player.jump()
    player.rect = player.rect.move(dx, dy)
    if pygame.sprite.spritecollideany(player, walls_group):
        player.rect = player.rect.move(-dx, -dy)

    npc_group.update()
    npc_group.draw(screen)
    walls_group.update()
    walls_group.draw(screen)
    pygame.display.flip() #отрисовка обьектов 
    dt = clock.tick(60) / 1000
    
pygame.quit()