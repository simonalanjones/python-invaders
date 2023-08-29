import pygame.sprite


class Invader(pygame.sprite.Sprite):
    def __init__(self, x, y, active, column, row, image_frames, index, points):
        super().__init__()

        self.index = index
        self.row = row
        self.column = column
        self.frame_pointer = 0
        self.image_frames = image_frames
        self.active = active
        self.points = points

        self.empty_frame = pygame.image.load(
            "sprites/invader/invader-empty-frame.png"
        ).convert_alpha()

        self.explode_frame = pygame.image.load(
            "sprites/invader/invader-explode.png"
        ).convert_alpha()

        # Create copies of the image frames to modify without affecting originals
        self.modified_frames = [frame.copy() for frame in self.image_frames]

        self.image = self.modified_frames[0]  # Start with the modified copy
        self.rect = self.image.get_rect(topleft=(x, y))

    def modify_pixel_colors(self):
        green = (0, 255, 0)
        white = (255, 255, 255)

        for frame in self.modified_frames:
            for y in range(frame.get_height()):
                for x in range(frame.get_width()):
                    pixel_color = frame.get_at((x, y))
                    if y + self.rect.y >= 191:
                        pixel_color.r, pixel_color.g, pixel_color.b = green
                    else:
                        pixel_color.r, pixel_color.g, pixel_color.b = white

                    frame.set_at((x, y), pixel_color)

    def explode(self):
        self.image = self.explode_frame
        self.active = False

    def release(self):
        self.kill()

    def move_across(self, direction):
        self.image = self.get_sprite_image()
        self.rect.x += direction

    def move_down(self, direction):
        self.image = self.get_sprite_image()
        self.rect.y += direction
        self.modify_pixel_colors()

    def get_sprite_image(self):
        self.frame_pointer = 1 - self.frame_pointer
        return self.modified_frames[self.frame_pointer]  # Use the modified copy

    def update(self):
        # ... (custom update behavior)
        pass
