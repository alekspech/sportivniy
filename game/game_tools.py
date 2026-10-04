import pygame

def round_vector(vector: pygame.math.Vector2):
    return pygame.math.Vector2(round(vector.x), round(vector.y))
    
