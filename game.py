import pygame
from pygame.locals import *

from classes.Game_controller import GameController
from classes.Config import Config

config = Config()
pygame.init()


game_controller = GameController(config)
running = True

while running:
    events = []
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        else:
            events.append(event)
    game_controller.update(events)
pygame.quit()
