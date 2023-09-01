import pygame.sprite

# global_position_threshold = 200


class ModifiedSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.original_image = image
        self.image = self.original_image.copy()  # Create a copy to modify
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.modify_pixel_colors()  # Modify pixel colors initially

    def modify_pixel_colors(self):
        pixel_array = pygame.PixelArray(self.image)
        for y in range(self.rect.height):
            for x in range(self.rect.width):
                global_x = self.rect.x + x
                global_y = self.rect.y + y

                if global_y > 150:
                    pixel_array[x, y] = (0, 255, 0, pixel_array[x, y][3])
        del pixel_array

    def update(self):
        # Handle updates here (e.g., changing position)
        # Modify pixel colors after each update
        self.modify_pixel_colors()
