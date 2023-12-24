import pygame
from lib.Controller import Controller
from classes.config.UI_config import UIConfig
from lib.Sprite_sheet import FontSpriteSheet
from lib.Sprite_sheet import PlayerSpriteSheet


class UIController(Controller):
    CANVAS_HEIGHT_PLAYER_LIVES = 8
    CANVAS_HEIGHT = 256
    CANVAS_WIDTH = 224

    def __init__(self):
        super().__init__()
        self.config = UIConfig()
        self.canvas_width = self.CANVAS_WIDTH
        self.canvas_height = self.CANVAS_HEIGHT
        self.canvas = pygame.Surface(
            (self.canvas_width, self.canvas_height), pygame.SRCALPHA
        )
        self.sprite_sheet = FontSpriteSheet()
        self.player_sprite_sheet = PlayerSpriteSheet()
        self.register_callback("get_score_text", self.create_text_surface)

    def text_generator(self, text_to_display):
        time_between_chars = 10  # Delay frames between each character
        char_index = 0
        frame_count = 0
        current_text = ""

        while char_index < len(text_to_display):
            if frame_count >= time_between_chars:
                current_text = text_to_display[: char_index + 1]
                yield current_text
                char_index += 1
                frame_count = 0
            else:
                yield current_text  # Return the progressively increasing text during the delay
            frame_count += 1

    def draw_lives(self):
        lives = self.callback("get_lives_count")
        player_base = self.player_sprite_sheet.get_sprite("player")
        # create a canvas the size of players
        if lives > 0:
            lives_canvas = pygame.Surface(
                (17 * lives, self.CANVAS_HEIGHT_PLAYER_LIVES), pygame.SRCALPHA
            )
            for i in range(lives - 1):
                lives_canvas.blit(player_base, (i * 16 + 12, 0))
        else:
            lives_canvas = pygame.Surface(
                (17, self.CANVAS_HEIGHT_PLAYER_LIVES), pygame.SRCALPHA
            )

        lives_remaining_canvas = self.create_text_surface(str(lives))
        lives_canvas.blit(lives_remaining_canvas, (0, 0))

        return lives_canvas

    def draw(self, surface):
        surface.blit(self.canvas, (0, 0))  # blit the canvas onto the game surface

    def update(self, events, state):
        # clear the canvas between each draw
        self.canvas.fill((0, 0, 0, 0))

        # get the score value using the callback to the scoreboard controller
        score = self.callback("get_score")

        # lives_canvas = self.draw_lives()
        # self.canvas.blit(lives_canvas, (1, 242))

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

        for idx, letter in enumerate(text):
            if not letter == " ":
                char_image = self.sprite_sheet.get_sprite(letter)
                text_surface.blit(char_image, (idx * 8, 0))

        return text_surface
