from lib.Game_sprite import GameSprite


class PlayerMissile(GameSprite):
    def __init__(self, params):
        super().__init__()

        self.delay = 1
        self.image = params.get("missile_sprite")
        self.explode_frame = params.get("explode_sprite")
        self.countdown = 0
        self.active = True
        self.rect = self.image.get_rect(
            x=params.get("player_x_position") + 8, y=params.get("player_y_position")
        )

    def draw(self, surface):
        surface.blit(self.modify_pixel_colors(self.image), self.rect)

    def remove(self):
        self.kill()

    def explode(self, position_rect=None):
        if self.active:
            self.image = self.explode_frame
            if position_rect:
                print("updated rect")
                self.rect.x = position_rect[0]
                self.rect.y = position_rect[1]

            # print(self.rect)
            # if position_rect
            # self.rect.x -= 4
            # self.rect.y -= 3
            self.active = False
            self.countdown = 30

    def update(self):
        if self.countdown > 0:
            self.countdown -= 1
            if self.countdown <= 0:
                self.kill()
        else:
            # if self.delay <= 0:
            self.delay = 1
            self.rect.y -= 4  # Move the missile vertically upwards
            if self.rect.y <= 42:
                self.explode(())
        # else:
        #   self.delay -= 1
        return self
