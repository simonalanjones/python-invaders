from classes.states.State_base import StateBase


class StateIntro(StateBase):
    def __init__(self):
        super().__init__()
        self.controllers = ["Invader", "Input", "Shield", "UI", "Baseline"]

    def enter(self, state_machine):
        super().enter(state_machine)
        self.add_listener("escape_button_pressed", self.on_escape_button_pressed)

    def on_escape_button_pressed(self, data):
        print("escape caught in state intro")
        self.exit("GAME_START")
