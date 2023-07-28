import os

base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class Config:
    config_values = {
        "original_screen_size": (224, 256),
        "larger_screen_size": (224 * 4, 256 * 4),
        "bg_image_path": os.path.join("images", "invaders_moon_bg.png"),
        "max_fps": 60,
        "top_left": (0, 0),
        # "font_path": os.path.join(base_directory, "space_invaders.ttf"),
        "shields": {
            "positions": [(29, 191), (75, 191), (127, 191), (173, 191)],
            "image": os.path.join("sprites", "player", "player-shield.png"),
        },
        "invaders": {
            "spawn_rows": [120, 144, 160, 168, 168, 168, 176, 176, 176],
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
        },
        "bombs": {
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
        },
    }

    @staticmethod
    def get(key):
        return Config.config_values.get(key)

    @staticmethod
    def get_file_path(key):
        return os.path.join(base_directory, key)
