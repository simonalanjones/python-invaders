import pygame
from classes.shield.Shield import Shield
from classes.config.Shield_config import ShieldConfig


class ShieldFactory:
    def __init__(self):
        config = ShieldConfig()
        image = config.get("image")
        image_path = config.get_file_path(image)

        self.shield_image = pygame.image.load(config.get_file_path(image_path))
        self.shield_positions = config.get("positions")

    def create_shields(self):
        sprite_group = pygame.sprite.Group()
        for position in self.shield_positions:
            x, y = position
            shield = Shield(x, y, self.shield_image)
            sprite_group.add(shield)
        return sprite_group
