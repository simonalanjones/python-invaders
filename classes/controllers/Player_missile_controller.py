from lib.Controller import Controller
from classes.models.Player_missile import PlayerMissile
from lib.Sprite_sheet import PlayerSpriteSheet
import pygame


class PlayerMissileController(Controller):
    def __init__(self):
        super().__init__()
        self.sprite_sheet = PlayerSpriteSheet()
        self.ready_flag = False
        # there will only ever be one sprite in this group
        self.missile_group = pygame.sprite.Group()

        self.register_callback("get_player_missile", self.get_player_missile)

        self.event_manager.add_listener("invader_removed", self.on_missile_ready)
        self.event_manager.add_listener("play_delay_complete", self.on_missile_ready)
        self.event_manager.add_listener("fire_button_pressed", self.on_fire_pressed)

    def game_ready(self):
        # self.get_invaders_callback = self.get_callback("get_invaders")
        self.get_player_callback = self.get_callback("get_player")
        self.mothership_is_exploding = self.get_callback("mothership_is_exploding")

    def on_missile_ready(self, data):
        self.ready_flag = True

    def on_fire_pressed(self, data):
        player = self.get_player_callback()
        if (
            not self.missile_group
            and self.ready_flag
            and not self.mothership_is_exploding()
        ):
            params = {
                "missile_sprite": self.sprite_sheet.get_sprite("missile"),
                "explode_sprite": self.sprite_sheet.get_sprite("missile_explode"),
                "player_x_position": player.rect.x,
                "player_y_position": player.rect.y,
            }
            self.missile_group.add(PlayerMissile(params))

    def check_collisions(self):
        if self.missile_group:
            collided_invaders = pygame.sprite.spritecollide(
                self.missile_group.sprites()[0], self.get_invaders_callback(), False
            )

            if collided_invaders:
                self.event_manager.notify("invader_hit", collided_invaders[0])
                self.ready_flag = False
                return True

    def update(self, events, dt):
        if self.missile_group:
            if not self.check_collisions():
                return self.missile_group.sprites()[0].update()
            else:
                self.missile_group.remove(self.missile_group.sprites()[0])

    # shields need access to player missile
    def get_player_missile(self):
        if self.missile_group:
            return self.missile_group.sprites()[0]

        # if self.player_missile:
        #     return self.player_missile.update()
        # else:
        #     print("nothing..")

        # if not self.countdown > 0:
        #     if self.player_missile:
        #         self.check_collisions()
        #         self.player_missile.rect.y -= 5
        #         if self.player_missile.rect.y <= 0:
        #             self.player_missile.explode()
        #             self.countdown = 15
        # else:
        #     print(self.countdown)
        #     self.countdown -= 1
        #     if self.countdown <= 0:
        #         self.player_missile = None
        #         self.ready_flag = True

        # return self.player_missile

    # def explode(self):
    #     self.countdown -= 1
    #     if self.countdown <= 0:
    #         self.player_missile = None
    #         self.ready_flag = True

    # def destroy_player_missile(self):
    #     self.player_missile = None
    #     self.ready_flag = True
