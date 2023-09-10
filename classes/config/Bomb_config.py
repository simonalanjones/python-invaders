import os
from classes.config.Base_config import BaseConfig


class BombConfig(BaseConfig):
    config_values = {
        "exploding_image": os.path.join(
            "sprites", "invader_bomb", "bomb_exploding.png"
        ),
        "images": {
            "plunger": [
                os.path.join("sprites", "invader_bomb", "plunger-frame1.png"),
                os.path.join("sprites", "invader_bomb", "plunger-frame2.png"),
                os.path.join("sprites", "invader_bomb", "plunger-frame3.png"),
                os.path.join("sprites", "invader_bomb", "plunger-frame4.png"),
            ],
            "squiggly": [
                os.path.join("sprites", "invader_bomb", "squiggly-frame1.png"),
                os.path.join("sprites", "invader_bomb", "squiggly-frame2.png"),
                os.path.join("sprites", "invader_bomb", "squiggly-frame3.png"),
                os.path.join("sprites", "invader_bomb", "squiggly-frame4.png"),
            ],
            "rolling": [
                os.path.join("sprites", "invader_bomb", "rolling-frame1.png"),
                os.path.join("sprites", "invader_bomb", "rolling-frame2.png"),
                os.path.join("sprites", "invader_bomb", "rolling-frame3.png"),
                os.path.join("sprites", "invader_bomb", "rolling-frame4.png"),
            ],
        },
        "max_bombs": 1,
        "grace_period": 60,
    }
