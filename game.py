import pygame, time
from pygame.locals import *

from classes.Game_controller import GameController
from classes.Config import Config

config = Config()
pygame.init()
last_time = time.time()


game_controller = GameController(config)
running = True

while running:
    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()

    events = []
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        else:
            events.append(event)
    game_controller.update(events, dt)
pygame.quit()
