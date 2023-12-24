from classes.controllers.UI_controller import UIController


class UIGameOverController(UIController):
    def __init__(self):
        super().__init__()

        self.game_over_message_position = (78, 48)
        self.game_over_text = "GAME OVER"

        self.game_over_text_iterator = self.text_generator(self.game_over_text)
        self.game_over_text_running = False

        self.event_manager.add_listener("game_ended", self.on_game_over)
        self.pause = 0

    def on_game_over(self, data):
        print("on game over")
        self.game_over_text_running = True

    def update(self, events, state):
        self.canvas.fill((0, 0, 0, 0))

        if self.game_over_text_running:
            try:
                current_text = next(self.game_over_text_iterator)
            except StopIteration:
                current_text = self.game_over_text

                self.pause += 1
                if self.pause == 180:
                    self.event_manager.notify("game_over_animation_ended")
                    self.game_over_text_running = False

            text_surface = self.create_text_surface(current_text)
            self.canvas.blit(text_surface, self.config.get("game_over_position"))

        return self
