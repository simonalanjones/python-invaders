import pygame
from classes.config.Bomb_config import BombConfig
from classes.bomb.Bomb import Bomb


class BombFactory:
    def __init__(self):
        config = BombConfig()
        self.bomb_frames = config.get("images")

        # Load bomb images using config into array
        for bomb_type, frames in self.bomb_frames.items():
            loaded_frames = []
            for frame in frames:
                image = pygame.image.load(config.get_file_path(frame))
                loaded_frames.append(image)
            self.bomb_frames[bomb_type] = loaded_frames

        self.exploding_frame = pygame.image.load(
            config.get("exploding_image")
        ).convert_alpha()

    def create_bomb(self, invader, bomb_type):
        x, y = invader.bomb_launch_position()

        bomb_sprite = Bomb(
            x, y, self.bomb_frames[bomb_type], self.exploding_frame, bomb_type
        )
        return bomb_sprite
