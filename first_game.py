import pygame
from varname.helpers import debug
import random

pygame.init()
screen = pygame.display.set_mode((1280,720)) #TODO вынести ширину и высоту экрана в переменные 
clock = pygame.time.Clock()
is_game_running = True
dt = 0

player_position = pygame.Vector2(
    # screen.get_width()/2,
    0,
    screen.get_height()/2,
) # spawn position
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
    player = pygame.draw.circle( 
        screen,
        player_color,
        player_position,
        radius = 20
    ) # cоздание игрока
    is_mouse_on_player = player.collidepoint(mouse_position)
    if is_mouse_on_player:
        player_color = 'red'
        player = pygame.draw.circle( 
            screen,
            player_color,
            player_position,
            radius = 20
        ) # cоздание игрока
    player_speed = 200
    

    player_speed = 200
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_position.y -= player_speed * dt 
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_position.y += player_speed * dt
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_position.x -= player_speed * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_position.x += player_speed * dt
    
    NPC_teammate_position = pygame.Vector2(
        player_position.x+30,
        player_position.y-20
    ) # spawn position
    NPC_teammate_color = 'red'
    NPC_teammate = pygame.draw.circle( 
            screen,
            NPC_teammate_color,
            NPC_teammate_position,
            radius = 20
        ) # cоздание игрока
    heal_color = 'yellow'
    heals_count = 20
    for heal_number in range(heals_count):
        if game_frame_number == 1:  
            heal_position = pygame.Vector2(
            random.randint(0,screen.get_width()),             
            random.randint(0,screen.get_height()),             
            )
            heal = pygame.draw.circle(
                surface=screen,
                color=heal_color,
                center=heal_position,
                radius=5
            )
            heals.append(heal)
        else:
            print(heal_number)
            heal = pygame.draw.circle(
                surface=screen,
                color=heal_color,
                center=(heals[heal_number].x,heals[heal_number].y),
                radius=5
            )

    is_mouse_on_NPC = player.collidepoint(mouse_position)
    # if is_mouse_on_NPC:
    pygame.display.flip() #отрисовка обьектов 
    dt = clock.tick(60) / 1000
    
pygame.quit()