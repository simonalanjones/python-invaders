import pygame.sprite


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, image_frames, explode_frame, bomb_type):
        super().__init__()
        self.image_frames = image_frames
        self.explode_frame = explode_frame
        self.direction = 2
        self.frame_counter = 0
        self.frame_pointer = 0
        self.bomb_type = bomb_type
        self.active = True
        self.countdown = 15

        # Create copies of the image frames to modify without affecting originals
        self.modified_frames = [frame.copy() for frame in self.image_frames]
        self.image = self.modified_frames[0]  # Start with the modified copy
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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

        if not self.bomb_type == "plunger":
            self.rect.y += 1
            self.rect.x -= 1
        else:
            self.rect.y += 2
            self.rect.x -= 2

        self.active = False
        self.countdown = 5

    def update(self):
        if self.active == True:
            self.frame_counter += 1
            if self.frame_counter >= 3:
                self.frame_counter = 0
                self.frame_pointer = (self.frame_pointer + 1) % len(self.image_frames)
                self.image = self.get_sprite_image()

            if self.rect.y <= 233:
                self.rect.y += 2 * 1.4  # 3 * 1.4
                self.modify_pixel_colors()
            # if self.rect.y > 232:
            #     self.rect.y = 232
            #     # self.kill()
        else:
            self.countdown -= 1
            if self.countdown == 0:
                self.kill()

    def get_sprite_image(self):
        return self.modified_frames[self.frame_pointer]  # Use the modified copy
