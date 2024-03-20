from classes.states.State_intro import StateIntro
from classes.states.State_game_starts import StateGameStarts
from classes.states.State_game_playing import StateGamePlaying
from classes.states.State_player_exploding import StatePlayerExploding
from classes.states.State_game_over import StateGameOver
from classes.states.State_post_game_over import StatePostGameOver


class StateMachine:
    def __init__(self):
        self.states = {
            "GAME_INTRO": StateIntro,
            "GAME_START": StateGameStarts,
            "GAME_PLAYING": StateGamePlaying,
            "PLAYER_EXPLODING": StatePlayerExploding,
            "GAME_OVER": StateGameOver,
            "POST_GAME_OVER": StatePostGameOver,
        }

        self.state = None
        self.change_to("GAME_START")

    def get_state_name(self):
        return self.state.name

    def has_valid_state(self):
        return self.state

    def get_state_controllers(self):
        if self.state:
            return self.state.controllers

    def change_to(self, new_state):
        if new_state in self.states:
            self.state = self.states[new_state]()
            self.enter_state()
        else:
            print(f"Invalid state change requested: {new_state}")

    def update(self, events):
        if self.state:
            self.state.update(events)

    def enter_state(self):
        self.state.enter(self.change_to)
