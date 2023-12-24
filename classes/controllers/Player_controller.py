import pygame
from lib.Controller import Controller
from classes.models.Player import Player

player_speed = 1

class PlayerController(Controller):
    def __init__(self):
        super().__init__()

        self.state = {}

        self.spawned = False
        self.is_exploding = False
        self.exploding_animation_complete = False

        # player group has one player sprite
        self.player_group_sprites = pygame.sprite.Group()

        

    def spawn_player(self):
        self.spawned = True
        params = {
            "player_x_position": 10,
            "player_y_position": 219,
        }
        player = Player(params)
        self.player_group_sprites.add(player)


    def explode_player(self):
        print("exploding player")
        self.is_exploding = True
        self.get_player().explode()


    def get_surface(self):
        return self.player_group_sprites

    def update(self, events, state):
        self.state = state
        self.check_bomb_collisions()
        if self.get_player():
             if 'player_enabled' in self.state:
                if self.state['player_enabled'] == True:
                    self.update_player()
                elif self.is_exploding:
                    self.get_player().update()
        else:
            if self.is_exploding:
                print("end of explosion")
                self.event_manager.notify("player_explosion_complete")
                self.exploding_animation_complete = True
                self.is_exploding = False


    def update_player(self):
        player = self.get_player()
        if self.state['is_moving_left']:
            player.rect.x -= player_speed
        elif self.state['is_moving_right']:
            player.rect.x += player_speed
        player.update()

    def clamp(value, min_value, max_value):
        return max(min(value, max_value), min_value)

    def get_player(self):
        if self.player_group_sprites.sprites():
            return self.player_group_sprites.sprites()[0]

    def check_bomb_collisions(self):
        if 'player_enabled' in self.state:
            if self.state['player_enabled'] == True:
                bomb_sprites = self.callback("get_bombs")

                if bomb_sprites is not None:
                    for bomb_sprite in bomb_sprites:
                        if bomb_sprite.active and pygame.sprite.collide_mask(
                            self.get_player(), bomb_sprite
                        ):
                            bomb_sprite.explode()
                        # print("here..")
                        # self.is_exploding = True
                        # self.player_enabled = False
                        # self.get_player().explode()
                            self.event_manager.notify("player_explodes")
