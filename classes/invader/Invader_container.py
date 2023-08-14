import pygame
from classes.invader.Invader_factory import InvaderFactory


class InvaderContainer(pygame.sprite.Group):
    def __init__(self, config):
        super().__init__()
        # copy the config values
        self.invader_direction = config.get("invaders")["horizontal_move"]
        self.invader_down_direction = config.get("invaders")["vertical_move"]
        self.screen_left_limit = config.get("invaders")["screen_left_limit"]
        self.screen_right_limit = config.get("invaders")["screen_right_limit"]
        self.screen_bottom_limit = config.get("invaders")["screen_bottom_limit"]
        # when an invader reaches the edge of the screen this flag is set
        self.invader_move_down = False
        # used to track which invader in the group is next to move
        self.current_invader_index = 0
        # flag used when invaders reach bottom of screen - game over
        self.invaders_landed = False

    def add_invader(self, invader):
        self.add(invader)

    def update(self):
        self.handle_invader_movement()
        self.update_current_invader_index()

    # remember last invader moves differently
    def handle_invader_movement(self):
        invader = self.get_invader_at_current_index()
        if invader and invader.active == True:
            if self.invader_move_down == False:
                invader.move_across(self.invader_direction)
            else:
                invader.move_down(self.invader_down_direction)

    def get_invader_at_current_index(self):
        all_sprites = self.sprites()
        if 0 <= self.current_invader_index < len(all_sprites):
            return all_sprites[self.current_invader_index]

    def update_current_invader_index(self):
        if self.current_invader_index < self.get_invader_count() - 1:
            self.current_invader_index += 1
        else:
            self.current_invader_index = 0
            self.update_movement_flags()

    def update_movement_flags(self):
        if self.invader_move_down == True:
            self.invader_move_down = False

        # check if any of the invaders have reached screen edge
        if self.has_reached_horizontal_limits():
            # if so switch the direction and set the move_down flag
            self.invader_direction = self.invader_direction * -1
            self.invader_move_down = True

        if self.has_reached_vertical_limit():
            self.invaders_landed = True

    def remove_inactive(self):
        for invader in self.get_invaders():
            if invader.active == False:
                self.remove_invader(invader)

    # def destroy_invader(self, invader):
    #     invader.explode()

    def remove_invader(self, invader):
        invader.active = False
        invader_index = invader.index

        self.remove(invader)
        for invader in self.get_invaders():
            if invader.index > invader_index:
                invader.index -= 1

        if invader_index < self.current_invader_index:
            self.current_invader_index -= 1
            # Decrement the indexes of the remaining invaders with higher indexes

        elif invader_index == self.current_invader_index:
            if self.current_invader_index >= self.get_invader_count():
                self.current_invader_index = 0

        else:
            if self.current_invader_index >= self.get_invader_count():
                self.current_invader_index = 0

    def get_invaders(self):
        # return [sprite for sprite in self.sprites() if sprite.active]
        return self.sprites()

    def get_invader_count(self) -> int:
        return len(self.sprites())

    def has_reached_vertical_limit(self) -> bool:
        for invader in self.sprites():
            if invader.rect.y + invader.rect.height >= self.screen_bottom_limit:
                return True
        return False

    def has_reached_horizontal_limits(self) -> bool:
        for invader in self.sprites():
            if (
                invader.rect.x >= self.screen_right_limit and self.invader_direction > 0
            ) or (
                invader.rect.x <= self.screen_left_limit and self.invader_direction < 0
            ):
                return True

        return False
