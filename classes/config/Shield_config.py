import os
from classes.config.Base_config import BaseConfig


class ShieldConfig(BaseConfig):
    config_values = {
        "positions": [(29, 191), (75, 191), (127, 191), (173, 191)],
        "image": os.path.join("sprites", "player", "player-shield.png"),
    }
