from classes.states.State_base import StateBase


class StateGamePlaying(StateBase):
    def __init__(self):
        super().__init__()
        self.controllers = [
            "Mothership",
            "Invader",
            "Input",
            "Shield",
            "Bomb",
            "Player",
            "PlayerMissile",
            "UI",
            "Baseline",
        ]

    def enter(self, change_to):
        super().enter(change_to)
        self.add_listener("player_explodes", self.on_player_hit)
        self.add_listener("invaders_landed", self.on_invaders_landed)

    def on_invaders_landed(self, data):
        print("invader landed in state")
        self.exit("PLAYER_EXPLODING")

    def on_player_hit(self, data):
        print("player was hit")
        self.exit("PLAYER_EXPLODING")
