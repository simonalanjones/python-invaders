from classes.models.Bomb import Bomb
from lib.Sprite_sheet import BombSpriteSheet


class BombFactory:
    def __init__(self):
        sprite_sheet = BombSpriteSheet()

        self.bomb_frames = {}
        self.bomb_frames["squiggly"] = [
            sprite_sheet.get_sprite("squiggly_frame1"),
            sprite_sheet.get_sprite("squiggly_frame2"),
            sprite_sheet.get_sprite("squiggly_frame3"),
            sprite_sheet.get_sprite("squiggly_frame4"),
        ]

        self.bomb_frames["rolling"] = [
            sprite_sheet.get_sprite("rolling_frame1"),
            sprite_sheet.get_sprite("rolling_frame2"),
            sprite_sheet.get_sprite("rolling_frame3"),
            sprite_sheet.get_sprite("rolling_frame4"),
        ]

        self.bomb_frames["plunger"] = [
            sprite_sheet.get_sprite("plunger_frame1"),
            sprite_sheet.get_sprite("plunger_frame2"),
            sprite_sheet.get_sprite("plunger_frame3"),
            sprite_sheet.get_sprite("plunger_frame4"),
        ]

        self.exploding_frame = sprite_sheet.get_sprite("explode_frame")

    def create_bomb(self, invader, bomb_type):
        x, y = invader.bomb_launch_position()

        bomb_sprite = Bomb(
            x, y, self.bomb_frames[bomb_type], self.exploding_frame, bomb_type
        )
        return bomb_sprite
