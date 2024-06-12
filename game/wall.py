import pygame
from varname.helpers import debug
import random

def generate_random_walls(screen_width, screen_height, num_segments):
    walls = pygame.sprite.Group()

    segment_width = screen_width // num_segments
    min_height = screen_height // 10
    max_height = screen_height // 2

    for i in range(num_segments):
        # Random height for the wall segment
        height = random.randint(min_height, max_height)
        y = screen_height - height  # Align the wall to the bottom of the screen

        # Randomly decide whether to create a gap
        if random.choice([True, False]):
            wall = Wall(i * segment_width, y, segment_width, height)
            walls.add(wall)
        else:
            # Create a smaller gap
            gap_height = random.randint(min_height, max_height // 2)
            wall1 = Wall(i * segment_width, 0, segment_width, y - gap_height)
            wall2 = Wall(i * segment_width, y + gap_height, segment_width, screen_height - (y + gap_height))
            walls.add(wall1)
            walls.add(wall2)

    return walls

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color='black'):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
