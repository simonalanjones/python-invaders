from lib.Controller import Controller
from classes.models.Player_missile import PlayerMissile
import pygame


class PlayerMissileController(Controller):
    def __init__(self):
        super().__init__()
        self.ready_flag = False
        self.rendering_order = 1
        # there will only ever be one sprite in this group
        self.missile_group = pygame.sprite.Group()

        self.register_callback("get_player_missile", self.get_player_missile)

        self.event_manager.add_listener("invader_removed", self.on_missile_ready)
        self.event_manager.add_listener("play_delay_complete", self.on_missile_ready)
        self.event_manager.add_listener("fire_button_pressed", self.on_fire_pressed)

    def game_ready(self):
        return

    def on_missile_ready(self, data):
        self.ready_flag = True

    def on_fire_pressed(self, data):
        if (
            not self.missile_group
            and self.ready_flag
            and not self.callback("mothership_is_exploding")
        ):
            player = self.callback("get_player")
            params = {
                "player_x_position": player.rect.x,
                "player_y_position": player.rect.y,
            }
            self.missile_group.add(PlayerMissile(params))

    def check_invader_collisions(self):
        if self.missile_group:
            invaders = self.callback("get_invaders")
            missile = self.get_player_missile()
            for invader_sprite in invaders:
                collision_area = pygame.sprite.collide_mask(invader_sprite, missile)
                if collision_area is not None:
                    self.event_manager.notify("invader_hit", invader_sprite)
                    self.ready_flag = False
                    return True

    def update(self, events, dt):
        if self.missile_group:
            if not self.check_invader_collisions():
                return self.get_player_missile().update()
            else:
                self.missile_group.remove(self.get_player_missile())

    # shields need access to player missile
    def get_player_missile(self):
        if self.missile_group:
            return self.missile_group.sprites()[0]
