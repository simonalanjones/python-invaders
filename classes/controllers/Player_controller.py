from lib.Controller import Controller
from classes.models.Player import Player
from lib.Sprite_sheet import PlayerSpriteSheet

player_speed = 1


class PlayerController(Controller):
    def __init__(self):
        super().__init__()
        self.can_launch_missile = True
        self.enabled = False
        sprite_sheet = PlayerSpriteSheet()

        params = {
            "player_sprite": sprite_sheet.get_sprite("player"),
            "player_explode_sprites": [
                sprite_sheet.get_sprite("player_explode1"),
                sprite_sheet.get_sprite("player_explode2"),
            ],
            "player_x_position": 10,
            "player_y_position": 218,
        }

        self.player = Player(params)

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
                # self.player.rect.x -= player_speed * dt
                self.player.rect.x -= player_speed
            elif self.right_key_pressed:
                # self.player.rect.x += player_speed * dt
                self.player.rect.x += player_speed
            return self.player

    def clamp(value, min_value, max_value):
        return max(min(value, max_value), min_value)

    def get_player(self):
        return self.player
