import pygame
from classes.models.Shield import Shield
from classes.config.Shield_config import ShieldConfig
from lib.Sprite_sheet import ShieldSpriteSheet


class ShieldFactory:
    def __init__(self):
        self.shield_image = ShieldSpriteSheet().get_sprite("shield_frame")
        self.shield_positions = ShieldConfig().get("positions")

    def create_shields(self):
        sprite_group = pygame.sprite.Group()
        for position in self.shield_positions:
            x, y = position
            shield = Shield(x, y, self.shield_image)
            sprite_group.add(shield)
        return sprite_group
