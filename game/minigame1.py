import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

bullet_image = pygame.Surface((40, 10), pygame.SRCALPHA)
pygame.draw.rect(bullet_image, (255, 0, 0), (0, 0, 40, 10))

player_position = pygame.math.Vector2(400, 300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30, 30, 30))

    mouse_position = pygame.math.Vector2(pygame.mouse.get_pos())
    shoot_direction = mouse_position - player_position

    if shoot_direction.length() != 0:
        shoot_direction = shoot_direction.normalize()

    # angle using Vector2.angle_to()
    right_vector = pygame.math.Vector2(1, 0)
    bullet_angle = -right_vector.angle_to(shoot_direction)  

    # rotate the bullet image
    rotated_bullet = pygame.transform.rotate(bullet_image, bullet_angle)
    rotated_rect = rotated_bullet.get_rect(center=player_position)

    # draw player
    pygame.draw.circle(screen, (0, 200, 255), player_position, 10)

    # draw shooting direction line
    line_end = player_position + shoot_direction * 100
    pygame.draw.line(screen, (0, 255, 0), player_position, line_end, 3)

    # draw right vector for reference
    right_end = player_position + right_vector * 100
    pygame.draw.line(screen, (255, 255, 0), player_position, right_end, 2)

    # draw the rotated bullet
    screen.blit(rotated_bullet, rotated_rect)

    # draw text angle
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Angle: {round(bullet_angle, 1)}°", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    text = font.render(f"Direction: {round(shoot_direction, 2)}°", True, (255, 255, 255))
    screen.blit(text, (10, 30))

    pygame.display.flip()
    clock.tick(60)
