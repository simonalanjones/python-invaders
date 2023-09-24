from lib.Game_sprite import GameSprite


class Player(GameSprite):
    def __init__(self, params):
        super().__init__()

        self.image = params.get("player_sprite")
        self.rect = self.image.get_rect(
            x=params.get("player_x_position"), y=params.get("player_y_position")
        )

    # used by BombController
    def get_rect(self):
        return self.rect

    def draw(self, surface):
        surface.blit(self.modify_pixel_colors(self.image), self.rect)
