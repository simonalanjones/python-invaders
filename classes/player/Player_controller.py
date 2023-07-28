# from pygame import KEYDOWN, KEYUP, K_a, K_d, K_l
import pygame
from pygame.locals import *
import sys

player_speed = 1


class PlayerController:
    def __init__(self, player, launch_missile_callback):
        self.player = player
        self.launch_missile_callback = launch_missile_callback
        self.can_launch_missile = True

    def update(self, events):
        self.move(events)

    # def update(self, events):
    #     for event in events:

    def move(self, events):
        # print(self.can_launch_missile)
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[K_LEFT]:
            dx -= player_speed
        if keys[K_RIGHT]:
            dx += player_speed
        if keys[K_SPACE] and self.can_launch_missile:
            print("launch!")
            self.pause_missile_launch()
            self.launch_missile_callback(self.player.get_rect())

        self.player.target_pos = (
            self.player.target_pos[0] + dx,
            self.player.target_pos[1] + dy,
        )

        # # Apply interpolation to make movement smoother
        self.player.rect.center = self.interpolate(
            self.player.rect.center, self.player.target_pos
        )

        # if event.type == KEYUP:
        #     if event.key == K_a:
        #         self.move_left()
        #     elif event.key == K_d:
        #         self.move_right()

        #     elif event.key == K_l and self.can_launch_missile:
        #         self.launch_missile_callback(self.player.get_rect())

    def interpolate(self, current_pos, target_pos):
        # Modify the interpolation_factor to change the smoothness of movement
        interpolation_factor = 0.2
        x = current_pos[0] + (target_pos[0] - current_pos[0]) * interpolation_factor
        y = current_pos[1] + (target_pos[1] - current_pos[1]) * interpolation_factor
        return int(x), int(y)

    def pause_missile_launch(self):
        self.can_launch_missile = False

    def resume_missile_launch(self):
        self.can_launch_missile = True

    # def move_left(self):
    #     # todo: check edge of screen
    #     self.player.rect.x -= 1

    # def move_right(self):
    #     # todo: check edge of screen
    #     self.player.rect.x += 1

    def destroy(self):
        # have this as callback
        pass

    def clamp(value, min_value, max_value):
        return max(min(value, max_value), min_value)

    def get_player(self):
        return self.player
