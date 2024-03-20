from classes.states.State_base import StateBase


class StateGameOver(StateBase):
    def __init__(self):
        super().__init__()
        self.controllers = [
            "Input",
            "Shield",
            "Bomb",
            "Player",
            "PlayerMissile",
            "UI",
            "UIGameOver",
            "Invader",
        ]

    def enter(self, state_machine):
        super().enter(state_machine)
        self.notify("game_ended")

        self.add_listener(
            "game_over_animation_ended", self.on_game_over_animation_ended
        )
        self.add_listener("wipe_animation_complete", self.on_wipe_animation_complete)

    def on_wipe_animation_complete(self, data):
        print("done wipe")
        self.exit("POST_GAME_OVER")

    def on_game_over_animation_ended(self, data):
        self.callback_manager.callback("begin_wipe_animation")
