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

        self.image = self.image_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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

    def get_sprite_image(self):
        self.frame_pointer = 1 - self.frame_pointer
        return self.image_frames[self.frame_pointer]
