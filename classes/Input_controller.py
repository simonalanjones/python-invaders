import pygame
from pygame.locals import *
from classes.Controller import Controller


# could be configured with allowed keys
# across different screens (game/highscore entry etc)
# maybe the init method could have a mode which would define the keys it tracks
# and it could be switched as well as set during config
class InputController(Controller):
    def __init__(self, config):
        super().__init__(config)

    def update(self, events, dt):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.event_manager.notify("escape_button_pressed")

                if event.key == K_k:  # 'K' key pressed
                    self.event_manager.notify("left_button_pressed")
                elif event.key == K_l:  # 'L' key pressed
                    self.event_manager.notify("right_button_pressed")
                elif event.key == K_SPACE:
                    self.event_manager.notify("fire_button_pressed")

            elif event.type == KEYUP:
                if event.key == K_k:  # 'K' key released
                    self.event_manager.notify("left_button_released")
                elif event.key == K_l:  # 'L' key released
                    self.event_manager.notify("right_button_released")
