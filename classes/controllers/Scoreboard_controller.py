from lib.Controller import Controller


class ScoreboardController(Controller):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.update_ui_callback = lambda: None

        self.register_callback("get_score", self.get_score)

        self.event_manager.add_listener("mothership_hit", self.on_points_awarded)
        self.event_manager.add_listener("points_awarded", self.on_points_awarded)

    def on_points_awarded(self, points):
        self.score += points
        if self.score >= 500 and self.callback("get_extra_life"):
            self.event_manager.notify("extra_life_awarded")

    def get_score(self):
        return str(self.score).zfill(5)
