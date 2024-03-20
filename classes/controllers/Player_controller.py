from lib.Controller import Controller
from classes.containers.Player_container import PlayerContainer


class PlayerController(Controller):
    def __init__(self):
        super().__init__()
        self.can_launch_missile = True
        self.movement_enabled = False
        self.left_key_pressed = False
        self.right_key_pressed = False

        self.lives = 3
        self.player_container = PlayerContainer()

        self.event_manager.add_listener("player_explodes", self.on_explode_player)
        self.event_manager.add_listener(
            "player_explosion_complete", self.on_player_explosion_complete
        )

        self.register_callback("spawn_player", self.spawn_player)
        self.register_callback("get_lives_count", lambda: self.lives)

        self.event_manager.add_listener("invaders_landed", self.on_invaders_landed)
        self.event_manager.add_listener(
            "entered_state_game_playing", self.on_game_starts
        )
        self.event_manager.add_listener("left_button_pressed", self.on_move_left)
        self.event_manager.add_listener("left_button_released", self.on_move_left_exit)
        self.event_manager.add_listener("right_button_pressed", self.on_move_right)
        self.event_manager.add_listener(
            "right_button_released", self.on_move_right_exit
        )

    def on_invaders_landed(self, data):
        self.on_explode_player(data)

    def on_game_starts(self, data):
        self.spawn_player()

    def on_player_explosion_complete(self, data):
        if self.lives > 0:
            self.lives -= 1

    def on_explode_player(self, data):
        self.movement_enabled = False
        self.right_key_pressed = False
        self.left_key_pressed = False

    def get_surface(self):
        return self.player_container

    def spawn_player(self):
        self.player_container.spawn_player()
        self.movement_enabled = True

    def on_move_left_exit(self, data):
        self.left_key_pressed = False

    def on_move_left(self, data):
        self.left_key_pressed = True

    def on_move_right_exit(self, data):
        self.right_key_pressed = False

    def on_move_right(self, data):
        self.right_key_pressed = True

    def update(self, events, dt=0):
        self.player_container.update()
        if self.get_player() and self.movement_enabled:
            return self.player_container.update_movement(
                self.left_key_pressed, self.right_key_pressed
            )

    # def update_player(self):
    #     return self.player_container.update(
    #         self.left_key_pressed, self.right_key_pressed
    #     )

    def get_player(self):
        return self.player_container.get_player()
