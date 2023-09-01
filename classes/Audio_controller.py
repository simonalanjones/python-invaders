import pygame
from classes.Controller import Controller
from classes.mothership.Mothership import Mothership

pygame.mixer.init()


class AudioController(Controller):
    def __init__(self, config):
        super().__init__(config)
        audio_config = config.get("audio")
        self.mothership_sound = pygame.mixer.Sound(audio_config["mothership"])
        self.mothership_bonus_sound = pygame.mixer.Sound(
            audio_config["mothership_bonus"]
        )

    def on_mothership_spawned(self, data):
        self.mothership_sound.play(-1)

    def on_mothership_exit(self, data):
        self.mothership_sound.fadeout(1000)

    def on_mothership_bonus(self, data):
        self.mothership_sound.stop()
        self.mothership_bonus_sound.play()

    def play_player_shot_sound(self):
        pass
