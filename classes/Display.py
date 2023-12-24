import pygame
from classes.config.Game_config import GameConfig


class Display:
    def __init__(self):
        config = GameConfig()
        self.top_left = config.get("top_left")
        self.original_screen_size = config.get("original_screen_size")
        self.larger_screen_size = config.get("larger_screen_size")

        _bg_image = pygame.image.load(config.get_file_path(config.get("bg_image_path")))
        self.scaled_image = pygame.transform.scale(_bg_image, self.larger_screen_size)
        self.window_surface = pygame.display.set_mode(self.larger_screen_size)

    def update(self, surface_array):
        clean_game_surface = pygame.Surface(self.original_screen_size, pygame.SRCALPHA)
        for drawable_surface in surface_array:
            # print(drawable_surface)
            if isinstance(drawable_surface, pygame.sprite.Group):
                # if isinstance(drawable_surface, pygame.Surface):
                drawable_surface.draw(clean_game_surface)

        # background image is drawn first
        self.window_surface.blit(self.scaled_image, self.top_left)

        # scale the playing surface up to target size on main window
        self.window_surface.blit(
            pygame.transform.scale(clean_game_surface, self.larger_screen_size),
            self.top_left,
        )
