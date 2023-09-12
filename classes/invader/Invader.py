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

        self.explode_frame = pygame.image.load(
            "sprites/invader/invader-explode.png"
        ).convert_alpha()

        # Create copies of the image frames to modify without affecting originals
        self.modified_frames = [frame.copy() for frame in self.image_frames]

        self.image = self.modified_frames[0]  # Start with the modified copy
        self.rect = self.image.get_rect(topleft=(x, y))

    def modify_pixel_colors(self):
        tints = [
            {"position": (0, 0), "size": (224, 32), "color": (255, 255, 255)},
            {"position": (0, 32), "size": (224, 32), "color": (255, 0, 0)},
            {"position": (0, 64), "size": (224, 120), "color": (255, 255, 255)},
            {"position": (0, 184), "size": (224, 56), "color": (0, 255, 0)},
            {"position": (0, 240), "size": (24, 16), "color": (255, 255, 255)},
            {"position": (24, 240), "size": (112, 16), "color": (0, 255, 0)},
            {"position": (136, 240), "size": (88, 16), "color": (255, 255, 255)},
        ]

        for frame in self.modified_frames:
            print(frame.get_width(), frame.get_height())
            for tint in tints:
                position = tint["position"]
                size = tint["size"]
                color = tint["color"]

                for y in range(position[1], position[1] + size[1]):
                    for x in range(position[0], position[0] + size[0]):
                        if 0 <= x < frame.get_width() and 0 <= y < frame.get_height():
                            pixel_color = frame.get_at((x, y))
                            pixel_color.r, pixel_color.g, pixel_color.b = color
                            frame.set_at((x, y), pixel_color)

    def _modify_pixel_colors(self):
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

    def bomb_launch_position(self):
        return (self.rect.x + 7, self.rect.y + 8)

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
