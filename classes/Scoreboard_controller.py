from classes.Controller import Controller


class ScoreboardController(Controller):
    def __init__(self, config):
        super().__init__(config)
        self.score = 0
        self.update_ui_callback = lambda: None

    def on_points_awarded(self, points):
        self.score += points

    def get_score(self):
        return str(self.score).zfill(5)
