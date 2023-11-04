import pygame
from lib.Controller import Controller
from classes.config.Audio_config import AudioConfig

pygame.mixer.init()


class AudioController(Controller):
    def __init__(self):
        super().__init__()
        config = AudioConfig()
        # print(config.config_values)
        self.mothership_sound = pygame.mixer.Sound(config.get("mothership"))
        self.mothership_bonus_sound = pygame.mixer.Sound(config.get("mothership_bonus"))
        self.player_explodes_sound = pygame.mixer.Sound(config.get("player_explodes"))
        self.extra_life_sound = pygame.mixer.Sound(config.get("extra_life"))

        self.event_manager.add_listener(
            "mothership_spawned", self.on_mothership_spawned
        )
        self.event_manager.add_listener("mothership_hit", self.on_mothership_bonus)

        self.event_manager.add_listener("mothership_exit", self.on_mothership_exit)
        self.event_manager.add_listener("player_explodes", self.on_player_explodes)
        self.event_manager.add_listener("extra_life_awarded", self.on_extra_life)

    def on_mothership_spawned(self, data):
        pass
        # self.mothership_sound.play(-1)

    def on_extra_life(self, data):
        self.extra_life_sound.play()

    def on_mothership_exit(self, data):
        self.mothership_sound.fadeout(1000)

    def on_mothership_bonus(self, data):
        self.mothership_sound.stop()
        self.mothership_bonus_sound.play()

    def on_player_explodes(self, data):
        self.player_explodes_sound.play()

    def play_player_shot_sound(self):
        pass
