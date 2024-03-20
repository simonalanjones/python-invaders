from classes.states.State_base import StateBase


class StateGameStarts(StateBase):
    def __init__(self):
        super().__init__()
        self.controllers = [
            "Invader",
            "Input",
            "Shield",
            "UI",
            "Baseline",
        ]
        self.play_delay = 0

    def enter(self, change_to):
        super().enter(change_to)
        self.add_listener("swarm_complete", self.on_swarm_complete)

    def on_swarm_complete(self, data):
        self.play_delay = 120

    def update(self, events):
        super().update(events)
        if self.play_delay > 0:
            self.play_delay -= 1
            if self.play_delay <= 0:
                self.exit("GAME_PLAYING")
