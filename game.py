import pygame
from pygame.locals import *
from classes.Game_controller import GameController
from classes.Config import Config


config = Config()
pygame.init()


class GameUtils:
    pass


# state machine class
game_controller = GameController(config)
running = True
# pygame.key.set_repeat(10, 20)  # Delay of 200ms and interval of 50ms

while running:
    events = []

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        else:
            events.append(event)
    game_controller.update(events)
pygame.quit()
