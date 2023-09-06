import pygame
from lib.Controller import Controller

pygame.mixer.init()


class AudioController(Controller):
    def __init__(self, config):
        super().__init__(config)
        audio_config = config.get("audio")
        self.mothership_sound = pygame.mixer.Sound(audio_config["mothership"])
        self.mothership_bonus_sound = pygame.mixer.Sound(
            audio_config["mothership_bonus"]
        )
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
