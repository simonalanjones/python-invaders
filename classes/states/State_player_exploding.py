from classes.states.State_base import StateBase


class StatePlayerExploding(StateBase):
    def __init__(self):
        super().__init__()
        self.controllers = [
            "Invader",
            "Shield",
            "Bomb",
            "Player",
            "PlayerMissile",
            "UI",
            "Baseline",
        ]

    def enter(self, change_to):
        super().enter(change_to)
        # these vars need reseting each time
        self.countdown_enabled = False
        self.play_delay = 0
        self.add_listener(
            "player_explosion_complete", self.on_player_explosion_complete
        )

    def on_player_explosion_complete(self, data):
        self.play_delay = 120
        self.countdown_enabled = True

    def update(self, events):
        super().update(events)
        if self.countdown_enabled:
            self.play_delay -= 1
            if self.play_delay <= 0:
                lives = self.callback_manager.callback("get_lives_count")
                if lives <= 0:
                    print("game over")
                    self.exit("GAME_OVER")
                else:
                    self.exit("GAME_PLAYING")
