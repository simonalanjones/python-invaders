import pygame


class GameSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def modify_pixel_colors(self, image):
        if isinstance(image, pygame.Surface):
            return self.apply_image_tints(image)
        else:
            print("not an image being converted")

    def apply_image_tints(self, image):
        area_colors = [0, 1, 0, 3, 0, 3, 0]  # Corresponding colors for each area
        areas = [
            {"position": (0, 0), "size": (224, 32)},
            {"position": (0, 32), "size": (224, 32)},
            {"position": (0, 64), "size": (224, 120)},
            {"position": (0, 184), "size": (224, 56)},
            {"position": (0, 240), "size": (24, 16)},
            {"position": (24, 240), "size": (112, 16)},
            {"position": (136, 240), "size": (88, 16)},
        ]

        # banding colours
        colors = [
            (255, 255, 255),  # White
            (255, 0, 0),  # Red
            (255, 255, 255),  # White
            (0, 255, 0),  # Green
            (255, 255, 255),  # White
            (0, 255, 0),  # Green
            (255, 255, 255),  # White
        ]

        for y in range(image.get_height()):
            for x in range(image.get_width()):
                pixel_color = image.get_at((x, y))
                pixel_x, pixel_y = (
                    self.rect.x + x,
                    self.rect.y + y,
                )  # Pixel position in the sprite's coordinate system

                for i, area in enumerate(areas):
                    area_rect = pygame.Rect(area["position"], area["size"])
                    if area_rect.collidepoint(pixel_x, pixel_y):
                        color_index = area_colors[i]
                        new_color = colors[color_index]
                        pixel_color.r, pixel_color.g, pixel_color.b = new_color

                image.set_at((x, y), pixel_color)

        return image
