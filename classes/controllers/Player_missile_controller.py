from lib.Controller import Controller
from classes.containers.Player_missile_container import PlayerMissileContainer


class PlayerMissileController(Controller):
    def __init__(self):
        super().__init__()
        self.ready_flag = False
        self.rendering_order = 1
        self.shot_counter = 0

        self.player_missile_container = PlayerMissileContainer()

        self.callback_manager.register_callback(
            "get_shot_counter", self.get_shot_counter
        )

        self.event_manager.add_listener("invader_hit", self.on_missile_not_ready)
        self.event_manager.add_listener("invader_removed", self.on_missile_ready)
        self.event_manager.add_listener(
            "entered_state_game_playing", self.on_missile_ready
        )
        self.event_manager.add_listener("fire_button_pressed", self.on_fire_pressed)
        self.event_manager.add_listener("mothership_exit", self.on_mothership_exit)

    def get_surface(self):
        return self.player_missile_container

    def get_shot_counter(self):
        return self.shot_counter

    def on_mothership_exit(self, data):
        self.shot_counter = 0

    def on_missile_not_ready(self, data):
        self.ready_flag = False

    def on_missile_ready(self, data):
        self.ready_flag = True

    def can_player_fire_missile(self):
        # and not self.callback("mothership_is_exploding")
        return (
            self.player_missile_container.find_missile_sprite() == None
            and self.ready_flag
            and not self.player_missile_container.find_missile_explosion()
        )

    def on_fire_pressed(self, data):
        if self.can_player_fire_missile():
            player = self.callback_manager.callback("get_player")
            params = {
                "player_x_position": player.rect.x,
                "player_y_position": player.rect.y,
            }
            self.player_missile_container.add_missile_sprite(params)
            self.shot_counter = (self.shot_counter + 1) % 16

    def update(self, events, dt=0):
        self.player_missile_container.update()
