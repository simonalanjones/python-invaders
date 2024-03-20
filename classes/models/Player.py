from lib.Game_sprite import GameSprite
from lib.Sprite_sheet import PlayerSpriteSheet

player_speed = 1


class Player(GameSprite):
    ANIMATION_FRAME_THRESHOLD_LOW = 5
    ANIMATION_FRAME_THRESHOLD_HIGH = 10
    MAX_ANIMATION_COUNT = 6

    def __init__(self, params):
        super().__init__()

        self.explosion_frame_number = 0
        self.explosion_animation_count = 0

        self.is_exploding = False
        self.sprite_sheet = PlayerSpriteSheet()
        self.image = self.sprite_sheet.get_sprite("player")

        self.exploding_images = [
            self.sprite_sheet.get_sprite("player_explode1"),
            self.sprite_sheet.get_sprite("player_explode2"),
        ]
        self.rect = self.image.get_rect(
            x=params.get("player_x_position"), y=params.get("player_y_position")
        )
        self.event_manager.add_listener("player_explodes", self.explode)
        # self.callback_manager.register_callback("get_player", self.get_player)

    def move_left(self):
        self.sprite.rect.x -= player_speed

    def move_right(self):
        self.sprite.rect.x += player_speed

    def update(self):
        if self.is_exploding:
            return self.update_exploding()
        else:
            return self.modify_pixel_colors(self.image)

    def explode(self, data):
        self.is_exploding = True
        self.image = self.exploding_images[0]

    def update_exploding(self):
        if self.explosion_animation_count < self.MAX_ANIMATION_COUNT:
            self.explosion_frame_number += 1
            if self.explosion_frame_number == self.ANIMATION_FRAME_THRESHOLD_LOW:
                self.image = self.exploding_images[1]
            elif self.explosion_frame_number == self.ANIMATION_FRAME_THRESHOLD_HIGH:
                self.image = self.exploding_images[0]
                self.explosion_frame_number = 0
                self.explosion_animation_count += 1
            return self.modify_pixel_colors(self.image)
        else:
            self.event_manager.notify("player_explosion_complete")
            self.kill()

    # used by BombController
    def get_rect(self):
        return self.rect
