import pygame
from pygame.locals import *
from lib.System import System

pygame.init()
system = System.get_instance()

running = True
max_fps = 60
clock = pygame.time.Clock()
while running:
    events = []
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        else:
            events.append(event)

    system.update(events)

    pygame.display.flip()
    clock.tick(max_fps)

pygame.quit()
