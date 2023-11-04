import pygame
from lib.Controller import Controller
from classes.models.Player import Player

player_speed = 1

# PLAY_DELAY_COMPLETE_EVENT = "play_delay_complete"
# LEFT_BUTTON_PRESSED_EVENT = "left_button_pressed"
# LEFT_BUTTON_RELEASED_EVENT = "left_button_released"
# RIGHT_BUTTON_PRESSED_EVENT = "right_button_pressed"
# RIGHT_BUTTON_RELEASED_EVENT = "right_button_released"
# PLAYER_EXPLOSION_COMPLETE_EVENT = "player_explosion_complete"


class PlayerController(Controller):
    def __init__(self):
        super().__init__()
        self.can_launch_missile = True
        self.enabled = False
        self.spawned = False
        self.is_exploding = False

        # player group has one player sprite
        self.player_group_sprites = pygame.sprite.Group()

        self.left_key_pressed = False
        self.right_key_pressed = False

        self.register_callback("get_player", self.get_player)
        self.register_callback("spawn_player", self.spawn_player)

        self.event_manager.add_listener(
            "play_delay_complete", self.on_play_delay_complete
        )
        self.event_manager.add_listener("left_button_pressed", self.on_move_left)
        self.event_manager.add_listener("left_button_released", self.on_move_left_exit)
        self.event_manager.add_listener("right_button_pressed", self.on_move_right)
        self.event_manager.add_listener(
            "right_button_released", self.on_move_right_exit
        )

    def spawn_player(self):
        self.spawned = True
        self.enabled = True
        params = {
            "player_x_position": 10,
            "player_y_position": 219,
        }
        player = Player(params)
        self.player_group_sprites.add(player)

    def on_play_delay_complete(self, data):
        self.spawn_player()

    def on_move_left_exit(self, data):
        self.left_key_pressed = False

    def on_move_left(self, data):
        self.left_key_pressed = True

    def on_move_right_exit(self, data):
        self.right_key_pressed = False

    def on_move_right(self, data):
        self.right_key_pressed = True

    def update(self, events, dt):
        self.check_bomb_collisions()
        if self.get_player():
            if self.enabled:
                return self.update_player()
            elif self.is_exploding:
                return self.get_player().update()

        else:
            if self.is_exploding:
                print("end of explosion")
                self.event_manager.notify("player_explosion_complete")
                self.is_exploding = False

    def update_player(self):
        player = self.get_player()
        if self.left_key_pressed:
            player.rect.x -= player_speed
        elif self.right_key_pressed:
            player.rect.x += player_speed
        return player.update()

    def clamp(value, min_value, max_value):
        return max(min(value, max_value), min_value)

    def get_player(self):
        if self.player_group_sprites.sprites():
            return self.player_group_sprites.sprites()[0]

    def check_bomb_collisions(self):
        if self.enabled:
            bomb_sprites = self.callback("get_bombs")

            if bomb_sprites is not None:
                for bomb_sprite in bomb_sprites:
                    if bomb_sprite.active and pygame.sprite.collide_mask(
                        self.get_player(), bomb_sprite
                    ):
                        bomb_sprite.explode()
                        print("hit")
                        self.is_exploding = True
                        self.enabled = False
                        self.get_player().explode()
                        self.event_manager.notify("player_explodes")
