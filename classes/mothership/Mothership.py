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
        self.explode_frame_count_max1 = 100  # max frames on initial sprite explod
        self.explode_frame_count_max1 = 200  # max frames showing score

    def explode(self, score_text_surface):
        self.active = False
        self.image = score_text_surface
        # self.image = pygame.image.load(self.sprite_path_explode).convert_alpha()

    def update(self, shot_counter, dt):
        if self.active:
            self.rect.x += self.direction * dt
            self.shot_counter = shot_counter
            if self.has_reached_screen_edge():
                self.kill()

        return self

    def calculate_points(self):
        return self.points_table[self.shot_counter]

    def has_reached_screen_edge(self):
        return (self.direction == 1 and self.rect.x > 224) or (
            self.direction == -1 and self.rect.x < 0
        )

    def draw(self, surface):
        # self.modify_pixel_colors()
        surface.blit(self.image, self.rect)
