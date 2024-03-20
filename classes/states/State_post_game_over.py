from classes.states.State_base import StateBase


class StatePostGameOver(StateBase):
    def __init__(self):
        super().__init__()
        self.controllers = [
            "Input",
            "UI",
            "Invader",
        ]

    def enter(self, state_machine):
        super().enter(state_machine)
        self.notify("game_ended")
        self.add_listener("escape_button_pressed", self.on_escape_button_pressed)

    def on_escape_button_pressed(self, data):
        print("escape caught in state post game")
        self.callback_manager.callback("clear_wipe")
        # self.exit("GAME_INTRO")
