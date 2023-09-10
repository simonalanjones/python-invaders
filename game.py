import pygame, time
from pygame.locals import *

from classes.Game_controller import GameController

pygame.init()


game_controller = GameController()
game_controller.load_controllers()
running = True
max_fps = 60
clock = pygame.time.Clock()
while running:
    dt = 0

    events = []
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        else:
            events.append(event)

    game_controller.update(events, dt)
    pygame.display.flip()
    clock.tick(max_fps)

pygame.quit()
