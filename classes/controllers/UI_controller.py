import pygame
from lib.Controller import Controller
from classes.config.UI_config import UIConfig


class UIController(Controller):
    def __init__(self):
        super().__init__()
        self.config = UIConfig()
        self.font_config = self.config.get("font_spritesheet_offsets")
        self.spritesheet = pygame.image.load("images/font_spritesheet.png")
        self.canvas_width = 224
        self.canvas_height = 256
        self.canvas = pygame.Surface(
            (self.canvas_width, self.canvas_height), pygame.SRCALPHA
        )

        self.register_callback("get_score_text", self.create_text_surface)
        self.get_score_callback = self.get_callback("get_score")

    def draw(self, surface):
        surface.blit(self.canvas, (0, 0))  # blit the canvas onto the game surface

    def update(self, events, dt):
        # clear the canvas between each draw
        self.canvas.fill((0, 0, 0, 0))
        # get the score value using the callback to the scoreboard controller
        score = str(self.get_score_callback())

        # position SCORE text at position in config
        self.canvas.blit(
            self.create_text_surface(self.config.get("score_label_text")),
            self.config.get("score_label_position"),
        )

        # position SCORE value at position in config
        text_surface = self.create_text_surface(score)
        self.canvas.blit(text_surface, self.config.get("score_value_position"))

        # position HI-SCORE text at position in config
        self.canvas.blit(
            self.create_text_surface(self.config.get("hiscore_label_text")),
            self.config.get("hiscore_label_position"),
        )

        # position HI-SCORE value at position in config
        text_surface = self.create_text_surface("00000")
        self.canvas.blit(text_surface, self.config.get("hiscore_value_position"))

        return self

    def create_text_surface(self, text):
        surface_width = len(text) * 8
        surface_height = 8
        text_surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)
        text_surface.fill((0, 0, 0, 0))

        # font_spritesheet_offsets = self.font_config.get("font_spritesheet_offsets")
        for idx, letter in enumerate(text):
            if letter in self.font_config:
                letter_x, letter_y = self.font_config[letter]
                letter_rect = pygame.Rect(letter_x, letter_y, 8, 8)
                letter_image = self.spritesheet.subsurface(letter_rect)
                text_surface.blit(letter_image, (idx * 8, 0))

        return text_surface
