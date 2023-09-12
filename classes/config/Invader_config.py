import os
from classes.config.Base_config import BaseConfig


class InvaderConfig(BaseConfig):
    config_values = {
        "spawn_rows": [170, 144, 160, 168, 168, 168, 176, 176, 176],
        "points": [30, 20, 20, 10, 10],
        "cols": 11,
        "rows": 5,
        "x_position_start": 16,
        "x_repeat_offset": 16,
        "y_repeat_offset": 17,
        "screen_bottom_limit": 218,
        "screen_left_limit": 25,
        "screen_right_limit": 200,
        "horizontal_move": 2,
        "vertical_move": 8,
        "images": {
            "small": [
                os.path.join("sprites", "invader", "invader-small-frame1.png"),
                os.path.join("sprites", "invader", "invader-small-frame2.png"),
            ],
            "mid": [
                os.path.join("sprites", "invader", "invader-mid-frame1.png"),
                os.path.join("sprites", "invader", "invader-mid-frame2.png"),
            ],
            "large": [
                os.path.join("sprites", "invader", "invader-large-frame1.png"),
                os.path.join("sprites", "invader", "invader-large-frame2.png"),
            ],
        },
    }
