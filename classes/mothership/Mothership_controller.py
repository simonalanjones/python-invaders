from classes.Controller import Controller
from classes.mothership.Mothership import Mothership
import pygame


class MothershipController(Controller):
    def __init__(self, config):
        super().__init__(config)
        self.shot_counter = 0
        self.config = config
        self.direction = None
        self.get_invaders_callback = lambda: None

    def on_update_shot_counter(self):
        self.shot_counter += 1
        if self.shot_counter > 15:
            self.shot_counter = 0

    # the score is dependant on the player shot count
    def get_score(self):
        bonus_score = self.config.get("mothership")["scores"][self.shot_counter]
        return bonus_score

    def set_spawn_position(self):
        pass
        # self.spawn_position =

    def set_spawn_direction(self):
        if self.shot_counter % 2 == 1:
            self.direction = -1
            # spawn position = self.config.get("mothership")["spawn_right_position"]
        else:
            self.direction = 1
            # spawn position = self.config.get("mothership")["spawn_left_position"]

    def spawn(self):
        pass

    # if get_tree().get_nodes_in_group('invader').size() >= 8:
