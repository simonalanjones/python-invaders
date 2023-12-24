from lib.Game_sprite import GameSprite


class Mothership(GameSprite):
    def __init__(
        self, mothership_image, explode_image, spawn_position, direction, points_table
    ):
        super().__init__()
        self.points_table = points_table
        self.image = mothership_image
        self.explode_image = explode_image
        self.rect = self.image.get_rect(topleft=spawn_position)
        self.direction = direction
        self.shot_counter = 0
        self.active = True
        self.explode_frame_count = 0
        self.points_image = None

    def explode(self, score_text_surface):
        # ensure the mothership is not partially shown on screen during explosion
        self.rect.x = min(self.rect.x, 208)
        self.active = False
        self.points_image = score_text_surface
        self.image = self.explode_image

    def update(self, shot_counter, dt):
        self.shot_counter = shot_counter
        if self.active:
            self.update_move(dt)
        else:
            self.update_exploding()
        return self

    def update_move(self, dt):
        self.rect.x += self.direction * 1

        if self.has_reached_screen_edge():
            self.kill()

    def update_exploding(self):
        self.explode_frame_count += 1
        if self.explode_frame_count == 20:
            self.image = self.points_image
        elif self.explode_frame_count == 92:
            self.kill()

    def calculate_points(self):
        return self.points_table[self.shot_counter]

    def has_reached_screen_edge(self):
        return (self.direction == 1 and self.rect.x > 224 - 17) or (
            self.direction == -1 and self.rect.x < 0
        )

    def draw(self, surface):
        surface.blit(self.modify_pixel_colors(self.image), self.rect)
