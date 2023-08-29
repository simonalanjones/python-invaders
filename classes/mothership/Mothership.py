import pygame.sprite


class Mothership(pygame.sprite.Sprite):
    def __init__(self, x, y, active, spawn_position, direction):
        super().__init__()
