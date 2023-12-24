import pygame, time
from pygame.locals import *

from states.State_intro import StateIntro
from states.State_game_starts import StateGameStarts
from states.State_game_playing import StateGamePlaying
from states.State_player_exploding import StatePlayerExploding
from classes.State_machine import StateMachine

pygame.init()

states = {
    "GAME_INTRO": StateIntro(),
    "GAME_START": StateGameStarts(),
    "GAME_PLAYING": StateGamePlaying(),
    "PLAYER_EXPLODING": StatePlayerExploding(),
}

# system = System()
state_machine = StateMachine(states, "GAME_INTRO")

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

    state_machine.update(events)

    pygame.display.flip()
    clock.tick(max_fps)

pygame.quit()
