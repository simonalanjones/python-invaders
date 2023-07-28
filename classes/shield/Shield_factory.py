import pygame
from classes.shield.Shield import Shield


class ShieldFactory:
    def __init__(self, config):
        image = config.get("shields")["image"]
        self.shield_image = pygame.image.load(config.get_file_path(image))
        self.shield_positions = config.get("shields")["positions"]

    def create_shields(self):
        sprite_group = pygame.sprite.Group()
        for position in self.shield_positions:
            x, y = position
            shield = Shield(x, y, self.shield_image)
            sprite_group.add(shield)
        return sprite_group
