import os

base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class Config:
    config_values = {
        "original_screen_size": (224, 256),
        "larger_screen_size": (224 * 4, 256 * 4),
        "bg_image_path": os.path.join("images", "invaders_moon_bg.png"),
        "max_fps": 60,
        "top_left": (0, 0),
        "ui": {
            "score_label_text": "SCORE",
            "score_label_position": (60, 16),
            "score_value_position": (60, 32),
            "hiscore_label_text": "HI-SCORE",
            "hiscore_label_position": (118, 16),
            "hiscore_value_position": (118, 32),
        },
        "shields": {
            "positions": [(29, 191), (75, 191), (127, 191), (173, 191)],
            "image": os.path.join("sprites", "player", "player-shield.png"),
        },
        "invaders": {
            "spawn_rows": [120, 144, 160, 168, 168, 168, 176, 176, 176],
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
        "mothership": {
            "image_frame": os.path.join("sprites", "mothership", "mothership.png"),
            "explode_frame": os.path.join(
                "sprites", "mothership", "mothership-exploding.png"
            ),
            # "cycles_with_explosion_frame": 60,
            # "cycles_with_bonus_text": 60,
            "cycles_until_spawn": 200,
            "qualifying_invader_y_position": 36,
            "spawn_left_position": (0, 48),
            "spawn_right_position": (224, 48),
            "points_table": [
                50,
                50,
                50,
                50,
                50,
                100,
                100,
                100,
                100,
                100,
                100,
                100,
                100,
                150,
                150,
                300,
            ],
        },
        "font_spritesheet_offsets": {
            "A": [1, 1],
            "B": [11, 1],
            "C": [21, 1],
            "D": [31, 1],
            "E": [41, 1],
            "F": [51, 1],
            "G": [61, 1],
            "H": [71, 1],
            "I": [1, 11],
            "J": [11, 11],
            "K": [21, 11],
            "L": [31, 11],
            "M": [41, 11],
            "N": [51, 11],
            "O": [61, 11],
            "P": [71, 11],
            "Q": [1, 21],
            "R": [11, 21],
            "S": [21, 21],
            "T": [31, 21],
            "U": [41, 21],
            "W": [51, 21],
            "X": [61, 21],
            "Y": [1, 31],
            "Z": [11, 31],
            "0": [21, 31],
            "1": [31, 31],
            "2": [41, 31],
            "3": [51, 31],
            "4": [61, 31],
            "5": [71, 31],
            "6": [1, 41],
            "7": [11, 41],
            "8": [21, 41],
            "9": [31, 41],
            "<": [41, 41],
            ">": [51, 41],
            "=": [61, 41],
            "*": [71, 41],
            "?": [1, 51],
            "-": [11, 51],
        },
        "audio": {
            "mothership": "sounds/mothership.wav",
            "mothership_bonus": "sounds/mothership_bonus.wav",
        },
    }

    @staticmethod
    def get(key):
        return Config.config_values.get(key)

    @staticmethod
    def get_file_path(key):
        return os.path.join(base_directory, key)
