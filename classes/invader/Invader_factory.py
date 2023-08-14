import pygame
from classes.invader.Invader import Invader


class InvaderFactory:
    def __init__(self, config):
        self.config = config
        invader_frames = config.get("invaders")["images"]

        # Load images and update invader_frames dictionary
        for invader_size, frames in invader_frames.items():
            loaded_frames = []
            for frame in frames:
                image = pygame.image.load(self.config.get_file_path(frame))
                loaded_frames.append(image)
            invader_frames[invader_size] = loaded_frames

        # invaders build from bottom up
        self.invader_build_array = [
            invader_frames["small"],
            invader_frames["mid"],
            invader_frames["mid"],
            invader_frames["large"],
            invader_frames["large"],
        ]

    def create_invader_swarm(self):
        spawn_rows_pointer = 0
        spawn_rows = self.config.get("invaders")["spawn_rows"]

        # number of invaders to draw horizontally
        invader_cols = self.config.get("invaders")["cols"]

        # number of invaders to draw vertically
        invader_rows = self.config.get("invaders")["rows"]

        # starting x position of invaders
        x_position_start = self.config.get("invaders")["x_position_start"]

        # horizontal offset between each invader
        x_repeat_offset = self.config.get("invaders")["x_repeat_offset"]

        # vertical offset between each invader
        y_repeat_offset = self.config.get("invaders")["y_repeat_offset"]

        # starting y position of invaders (change with each wave cleared)
        y_position_start = spawn_rows[spawn_rows_pointer]
        index = 0

        for y_position in range(invader_rows):
            for x_position in range(invader_cols):
                yield self.create_invader(
                    x_position_start + (x_position * x_repeat_offset),
                    y_position_start - (y_position * y_repeat_offset),
                    True,
                    x_position,
                    4 - y_position,
                    index,
                )

                index += 1

    def create_invader(self, x, y, active, column, row, index):
        points_array = self.config.get("invaders")["points"]
        points_for_row = points_array[row]
        # points = self.config.get("invaders")[row]
        invader_sprite = Invader(
            x,
            y,
            active,
            column,
            row,
            self.invader_build_array[row],
            index,
            points_for_row,
        )
        return invader_sprite
