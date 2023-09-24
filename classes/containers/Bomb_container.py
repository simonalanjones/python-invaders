import pygame
from classes.models.Bomb import Bomb


class BombContainer(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def notify_collision(self, bomb):
        if isinstance(bomb, Bomb):
            bomb.active = False

    def update(self):
        # Update all existing bomb sprites in this container
        for sprite in self.sprites():
            sprite.update()

    def get_bombs(self):
        return [bomb for bomb in self.sprites() if bomb.active]

    def has_rolling_shot(self):
        return any(bomb.bomb_type == "rolling" for bomb in self.sprites())
