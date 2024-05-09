import pygame

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
running = True
dt = 0

player_position = pygame.Vector2(
    screen.get_width()/2,
    screen.get_height()/2,
)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill('blue')
    pygame.draw.circle(
        screen,
        'green',
        player_position,
        radius = 20
    )
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_position.y -= 300 * dt
    if keys[pygame.K_s]:
        player_position.y += 300 * dt
    if keys[pygame.K_a]:
        player_position.x -= 300 * dt
    if keys[pygame.K_d]:
        player_position.x += 300 * dt

    pygame.display.flip()
    dt = clock.tick(60) / 1000
    print(dt)

pygame.quit()