import pygame
from lib.Controller import Controller
from classes.config.Audio_config import AudioConfig

pygame.mixer.init()


class AudioController(Controller):
    def __init__(self):
        super().__init__()
        config = AudioConfig()
        self.mothership_sound = pygame.mixer.Sound(config.get("mothership"))

        self.mothership_bonus_sound = pygame.mixer.Sound(config.get("mothership_bonus"))
        self.event_manager.add_listener(
            "mothership_spawned", self.on_mothership_spawned
        )
        self.event_manager.add_listener("mothership_hit", self.on_mothership_bonus)

        self.event_manager.add_listener("mothership_exit", self.on_mothership_exit)

    def on_mothership_spawned(self, data):
        pass
        # self.mothership_sound.play(-1)

    def on_mothership_exit(self, data):
        self.mothership_sound.fadeout(1000)

    def on_mothership_bonus(self, data):
        self.mothership_sound.stop()
        self.mothership_bonus_sound.play()

    def play_player_shot_sound(self):
        pass
