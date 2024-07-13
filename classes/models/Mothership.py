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
        self.active = True
        self.explode_frame_count = 0

    def explode(self, score_text_surface=None):
        # ensure the mothership is not partially shown on screen during explosion
        self.rect.x = min(self.rect.x, 208)
        self.active = False
        self.image = self.explode_image

    def update(self):
        if self.active:
            self.update_move()
        else:
            self.update_exploding()
        return self

    def update_move(self):
        self.rect.x += self.direction * 1

        if self.has_reached_screen_edge():
            self.event_manager.notify("mothership_exit")
            self.kill()

    def update_exploding(self):
        self.explode_frame_count += 1

        # change from exploding image to points image after 20 cycles
        if self.explode_frame_count == 20:
            shots = self.get_shot_counter()
            points = self.calculate_points(shots)
            if points > 0:
                points_text_image = self.callback_manager.callback(
                    "get_score_text", str(points)
                )
                self.image = points_text_image

        # after 92 cycles remove the mothership
        elif self.explode_frame_count == 92:
            self.kill()

    def get_shot_counter(self):
        if self.callback_manager.callback_exists("get_shot_counter"):
            return self.callback_manager.callback("get_shot_counter")

    def calculate_points(self, shots):
        return self.points_table[shots]

    def has_reached_screen_edge(self):
        return (self.direction == 1 and self.rect.x > 224 - 17) or (
            self.direction == -1 and self.rect.x < 0
        )
