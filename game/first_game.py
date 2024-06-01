import pygame
from varname.helpers import debug
import random
from game.player import PlayerKapibara

pygame.init()
screen = pygame.display.set_mode((1280,720)) #TODO вынести ширину и высоту экрана в переменные 
clock = pygame.time.Clock()
is_game_running = True
dt = 0
player_speed = 200
player_img_path = 'textures/kapibara.jpeg'
player = PlayerKapibara(img_path=player_img_path)
npc_group = pygame.sprite.Group()
npc_group.add(player)
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

    # is_mouse_on_player = player.collidepoint(mouse_position)
    # if is_mouse_on_player:
    #     player_color = 'red'
    #     player = pygame.draw.circle( 
    #         screen,
    #         player_color,
    #         player_position,
    #         radius = 20
    #     ) # cоздание игрокa
    

    keys = pygame.key.get_pressed()
    dx = 0
    dy = 0 #премешение игрока по иксу и по игрику
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        dy -= player_speed * dt 
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dy += player_speed * dt
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        dx -= player_speed * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        dx += player_speed * dt
    player.rect = player.rect.move(dx, dy)
    npc_group.update()
    npc_group.draw(screen)
    # NPC_teammate_position = pygame.Vector2(
    #     player_position.x+30,
    #     player_position.y-20
    # ) # spawn position
    # NPC_teammate_color = 'red'
    # NPC_teammate = pygame.draw.circle( 
    #         screen,
    #         NPC_teammate_color,
    #         NPC_teammate_position,
    #         radius = 20
    #     ) # cоздание игрока
    # heal_color = 'yellow'
    # heals_count = 20
    # for heal_number in range(heals_count):
    #     if game_frame_number == 1:  
    #         heal_position = pygame.Vector2(
    #         random.randint(0,screen.get_width()),             
    #         random.randint(0,screen.get_height()),             
    #         )
    #         heal = pygame.draw.circle(
    #             surface=screen,
    #             color=heal_color,
    #             center=heal_position,
    #             radius=5
    #         )
    #         heals.append(heal)
    #     else:
    #         print(heal_number)
    #         heal = pygame.draw.circle(
    #             surface=screen,
    #             color=heal_color,
    #             center=(heals[heal_number].x,heals[heal_number].y),
    #             radius=5
    #         )

    # is_mouse_on_NPC = player.collidepoint(mouse_position)
    # player.collideobjects(heals)
    # if is_mouse_on_NPC:
    pygame.display.flip() #отрисовка обьектов 
    dt = clock.tick(60) / 1000
    
pygame.quit()