from lib.Game_sprite import GameSprite
from lib.Sprite_sheet import PlayerSpriteSheet


class PlayerMissile(GameSprite):
    def __init__(self, params):
        super().__init__()

        sprite_sheet = PlayerSpriteSheet()
        self.image = sprite_sheet.get_sprite("missile")
        self.explode_frame = sprite_sheet.get_sprite("missile_explode")

        self.countdown = 0
        self.active = True
        self.rect = self.image.get_rect(
            x=params.get("player_x_position") + 8, y=params.get("player_y_position")
        )

    def draw(self, surface):
        # surface.blit(self.image, self.rect)
        surface.blit(self.modify_pixel_colors(self.image), self.rect)

    def remove(self):
        self.kill()

    def explode(self, offset_rect=None):
        if self.active:
            self.image = self.explode_frame
            if offset_rect:
                self.rect = self.rect.move(offset_rect)

            self.active = False
            self.countdown = 15

    def update(self):
        if self.countdown > 0:
            self.countdown -= 1
            if self.countdown <= 0:
                self.kill()
        else:
            self.rect.y -= 4  # Move the missile vertically upwards
            if self.rect.y <= 42:
                self.explode(())

        return self
