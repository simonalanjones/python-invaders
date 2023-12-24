import pygame
from classes.config.Invader_config import InvaderConfig


class InvaderContainer(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        config = InvaderConfig()
        # copy the config values
        self.invader_direction = config.get("horizontal_move")
        self.invader_down_direction = config.get("vertical_move")
        self.screen_left_limit = config.get("screen_left_limit")
        self.screen_right_limit = config.get("screen_right_limit")
        self.screen_bottom_limit = config.get("screen_bottom_limit")
        # when an invader reaches the edge of the screen this flag is set
        self.invaders_moving_down = False
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
        if invader and invader.active:
            if not self.invaders_moving_down:
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
        if self.invaders_moving_down == True:
            self.invaders_moving_down = False

        # check if any of the invaders have reached screen edge
        if self.has_reached_horizontal_limits():
            # if so switch the direction and set the move_down flag
            self.invader_direction = self.invader_direction * -1
            self.invaders_moving_down = True

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

    def get_invaders_with_clear_path(self):
        invaders_with_clear_path = []
        invader_group = self.sprites()
        # find the lowest screen row (initially row 4) of remaining invaders
        # invaders on this row number won't need a path check
        max_row = max(invader_group, key=lambda invader: invader.row).row

        for invader in invader_group:
            clear_path = True

            # if the invader is on the lowest screen row (highest row number) then don't check any further
            if invader.row == max_row:
                invaders_with_clear_path.append(invader)
                continue

            # else begin inner loop:
            # check all invaders against the invader in the outer loop
            # if there is an invader with the same column (as the outer loop invader)
            # but on a lower screen row (higher row number) then it's not a clear path
            for _invader in invader_group:
                if _invader.column == invader.column and _invader.row > invader.row:
                    clear_path = False
                    break

            if clear_path:
                invaders_with_clear_path.append(invader)

        return invaders_with_clear_path

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
