import os


class Config:
    config_values = {
        "original_screen_size": (224, 256),
        "larger_screen_size": (224 * 4, 256 * 4),
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
        },
        "bombs": {
            "max_bombs": 1,
            "grace_period": 60,
        },
        "mothership": {
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
        "audio": {
            "mothership": "sounds/mothership.wav",
            "mothership_bonus": "sounds/mothership_bonus.wav",
            "player_explodes": "sounds/player_destroyed.wav",
        },
    }

    @staticmethod
    def get(key):
        return Config.config_values.get(key)
