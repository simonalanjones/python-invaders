from lib.Game_sprite import GameSprite
from lib.Sprite_sheet import PlayerSpriteSheet


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

    def update(self):
        if self.is_exploding:
            return self.update_exploding()
        else:
            return self

    def explode(self):
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
            return self
        else:
            self.kill()

    # used by BombController
    def get_rect(self):
        return self.rect

    def draw(self, surface):
        surface.blit(self.modify_pixel_colors(self.image), self.rect)
