import pygame.sprite


class Mothership(pygame.sprite.Sprite):
    def __init__(self, spawn_position, direction, points_table):
        super().__init__()
        self.sprite_path = "sprites/mothership/mothership.png"
        self.sprite_path_explode = "sprites/mothership/mothership-exploding.png"
        self.points_table = points_table
        self.image = pygame.image.load(self.sprite_path).convert_alpha()
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
        self.image = pygame.image.load(self.sprite_path_explode).convert_alpha()

    def update(self, shot_counter, dt):
        self.shot_counter = shot_counter
        if self.active:
            self.update_move(dt)
        else:
            self.update_exploding()
        return self

    def update_move(self, dt):
        self.rect.x += self.direction * dt

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
        self.modify_pixel_colors()
        surface.blit(self.image, self.rect)

    # in the arcade game a red filter was applied
    def modify_pixel_colors(self):
        red = (255, 0, 0)
        white = (255, 255, 255)
        for y in range(self.image.get_height()):
            for x in range(self.image.get_width()):
                pixel_color = self.image.get_at((x, y))
                if (
                    pixel_color[0] == 255
                    and pixel_color[1] == 255
                    and pixel_color[2] == 255
                ):
                    pixel_color.r, pixel_color.g, pixel_color.b = red
                    self.image.set_at((x, y), pixel_color)
