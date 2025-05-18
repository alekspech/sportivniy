import pygame
from varname.helpers import debug
import random

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.world_position = pygame.math.Vector2(x,y)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 50
        
    def draw(self, screen, camera_offset):
        screen_position = self.world_position - camera_offset
        screen.blit(self.image, screen_position)

    def wall_collide_bullet(self, bullets_group):
        bullet = pygame.sprite.spritecollideany(self, bullets_group)
        if bullet is not None:
            print('collide wall')
            bullet_damage = bullet.damage
            bullet_position = bullet.rect.center
            bullets_group.remove(bullet)
            self.hp -= bullet_damage
            if self.hp < 0:
                self.hp = 0
    
    def update(self, bullets_group):
        self.wall_collide_bullet(bullets_group)

    def draw_hp(self, screen, camera_offset):
        hp_position = self.world_position - camera_offset
        hp_position.y -= int(self.rect.height * 3/4)      
        text_generator = pygame.font.SysFont('Comic Sans MS', size=20)
        text = text_generator.render(
            '{}'.format(self.hp), 1,(255,0,0)
        )
        screen.blit(text, dest = hp_position)

def generate_walls():
    walls_group = pygame.sprite.Group()

    # Define parameters
    level_height = 450  # Vertical distance between levels
    platform_length = 3000  # Total horizontal space per level
    sections_per_level = 4  # How many platforms in X direction per level
    gap_width = 300  # Horizontal gap between platforms
    platform_thickness = 10  # Thickness of each platform

    num_levels_y = 12

    section_width = (platform_length - (gap_width * (sections_per_level - 1))) / sections_per_level

    for i in range(num_levels_y):
        y = i * level_height

        for j in range(sections_per_level):
            x_start = j * (section_width + gap_width)
            x_end = x_start + section_width

            wall = create_wall_from_points(x_start, y, x_end, y + platform_thickness, color='black')
            walls_group.add(wall)

    return walls_group

def create_wall_from_points(x1, y1, x2, y2, color):
    x = min(x1, x2)
    y = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    return Wall(x, y, width, height, color)