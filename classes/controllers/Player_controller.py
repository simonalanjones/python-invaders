from lib.Controller import Controller
from classes.player.Player import Player

player_speed = 1


class PlayerController(Controller):
    def __init__(self, config):
        super().__init__(config)
        self.can_launch_missile = True
        self.enabled = False
        self.player = Player()

        self.left_key_pressed = False
        self.right_key_pressed = False

        self.register_callback("get_player", self.get_player)

        self.event_manager.add_listener(
            "play_delay_complete", self.on_play_delay_complete
        )
        self.event_manager.add_listener("left_button_pressed", self.on_move_left)
        self.event_manager.add_listener("left_button_released", self.on_move_left_exit)
        self.event_manager.add_listener("right_button_pressed", self.on_move_right)
        self.event_manager.add_listener(
            "right_button_released", self.on_move_right_exit
        )

    def on_play_delay_complete(self, data):
        self.enabled = True

    def on_move_left_exit(self, data):
        self.left_key_pressed = False

    def on_move_left(self, data):
        self.left_key_pressed = True

    def on_move_right_exit(self, data):
        self.right_key_pressed = False

    def on_move_right(self, data):
        self.right_key_pressed = True

    def update(self, events, dt):
        if self.enabled:
            if self.left_key_pressed:
                self.player.rect.x -= player_speed * dt
            elif self.right_key_pressed:
                self.player.rect.x += player_speed * dt
            return self.player

    def clamp(value, min_value, max_value):
        return max(min(value, max_value), min_value)

    def get_player(self):
        return self.player
