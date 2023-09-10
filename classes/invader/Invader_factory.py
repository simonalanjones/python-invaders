import os
import pygame
from classes.invader.Invader import Invader
from classes.config.Invader_config import InvaderConfig


class InvaderFactory:
    def __init__(self):
        config = InvaderConfig()

        self.invader_frame_paths = config.get("images")

        self.points_array = config.get("points")
        self.spawn_rows = config.get("spawn_rows")

        self.invader_cols = config.get("cols")

        # number of invaders to draw vertically
        self.invader_rows = config.get("rows")

        # starting x position of invaders
        self.x_position_start = config.get("x_position_start")

        # horizontal offset between each invader
        self.x_repeat_offset = config.get("x_repeat_offset")

        # vertical offset between each invader
        self.y_repeat_offset = config.get("y_repeat_offset")

        # store a reference to the function in the config
        self.get_file_path = config.get_file_path

        invader_frames = self.load_invader_images()

        # invaders build/drawn upwards on screen
        self.invader_build_array = [
            invader_frames["small"],
            invader_frames["mid"],
            invader_frames["mid"],
            invader_frames["large"],
            invader_frames["large"],
        ]

    def load_invader_images(self):
        invader_frames = self.invader_frame_paths
        invader_images = {}

        for invader_size, frames in invader_frames.items():
            loaded_frames = []
            for frame in frames:
                _image_path = self.get_file_path(frame)
                try:
                    image = pygame.image.load(_image_path).convert_alpha()
                    loaded_frames.append(image)
                except pygame.error as e:
                    print(f"Error loading image: {_image_path}")

            invader_images[invader_size] = loaded_frames

        return invader_images

    def create_invader_swarm(self):
        spawn_rows_pointer = 0

        # starting y position of invaders (change with each wave cleared)
        y_position_start = self.spawn_rows[spawn_rows_pointer]
        index = 0

        for y_position in range(self.invader_rows):
            for x_position in range(self.invader_cols):
                yield self.create_invader(
                    self.x_position_start + (x_position * self.x_repeat_offset),
                    y_position_start - (y_position * self.y_repeat_offset),
                    True,
                    x_position,
                    4 - y_position,
                    index,
                    self.points_array[4 - y_position],
                )

                index += 1

    def create_invader(self, x, y, active, column, row, index, points):
        invader_sprite = Invader(
            x,
            y,
            active,
            column,
            row,
            self.invader_build_array[row],
            index,
            points,
        )
        return invader_sprite
