import os
from classes.config.Base_config import BaseConfig


class AudioConfig(BaseConfig):
    config_values = {
        "mothership": "sounds/mothership.wav",
        "mothership_bonus": "sounds/mothership_bonus.wav",
        "player_explodes": "sounds/player_destroyed.wav",
        "extra_life": "sounds/extra_life.wav",
    }
