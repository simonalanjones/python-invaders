import pygame
from classes.bomb.Bomb import Bomb


class BombFactory:
    def __init__(self, config):
        self.config = config
        self.bomb_frames = config.get("bombs")["images"]

        # Load bomb images using config into array
        for bomb_type, frames in self.bomb_frames.items():
            loaded_frames = []
            for frame in frames:
                image = pygame.image.load(self.config.get_file_path(frame))
                loaded_frames.append(image)
            self.bomb_frames[bomb_type] = loaded_frames

        self.explode_frame = pygame.image.load(
            "sprites/invader_bomb/bomb_exploding.png"
        ).convert_alpha()

    def create_bomb(self, invader, bomb_type):
        x = invader.rect.x + 7
        y = invader.rect.y + 8

        bomb_sprite = Bomb(
            x, y, self.bomb_frames[bomb_type], self.explode_frame, bomb_type
        )
        return bomb_sprite
