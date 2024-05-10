import pygame
from varname.helpers import debug

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

while is_game_running: # основной цикл игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game_running = False

    screen.fill('blue')
    mouse_position = pygame.mouse.get_pos()
    debug(mouse_position)
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
    

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_position.y -= player_speed * dt 
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_position.y += player_speed * dt
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_position.x -= player_speed * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_position.x += player_speed * dt


    pygame.display.flip()
    dt = clock.tick(60) / 1000


pygame.quit()