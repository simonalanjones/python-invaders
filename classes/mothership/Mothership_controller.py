from classes.Controller import Controller
from classes.mothership.Mothership import Mothership
import pygame


class MothershipController(Controller):
    def __init__(self, config):
        super().__init__(config)
        mothership_config = config.get("mothership")

        self.spawned = False
        self.shot_counter = 0
        self.config = config
        self.direction = None
        self.get_invaders_callback = lambda: None

        self.cycles_until_spawn = mothership_config["cycles_until_spawn"]
        self.qualifying_invader_y_position = mothership_config[
            "qualifying_invader_y_position"
        ]
        self.points_table = mothership_config["points_table"]

        self.cycles_lapsed = 0
        self.ready_flag = (
            False  # flag to identify that invaders have reached low enough position
        )
        self.mothership_group = pygame.sprite.Group()

    def update(self, events, dt):
        # if no mothership spawned
        if not self.spawned:
            self.cycles_lapsed += 1

            # periodically check that invaders are low enough before mothership is spawn ready
            if self.cycles_lapsed == 60 and self.check_invaders_position():
                self.ready_flag = True

            if self.cycles_lapsed == self.cycles_until_spawn:
                if self.ready_flag:
                    self.spawn()
                else:
                    self.cycles_lapsed = 0

        else:
            if self.mothership_group.sprites():
                mothership = self.mothership_group.sprites()[0]
                return mothership.update(self.shot_counter, dt)
            else:
                self.shot_counter = 0
                self.cycles_lapsed = 0  # Reset the counter after spawning
                self.spawned = False

    def check_invaders_position(self):
        invaders = self.get_invaders_callback()
        highest_y = max(sprite.rect.y for sprite in invaders)
        return highest_y >= self.qualifying_invader_y_position

    def on_update_shot_counter(self, data):
        self.shot_counter = (self.shot_counter + 1) % 16

    def set_spawn_direction(self):
        if self.shot_counter % 2 == 1:
            self.direction = -1
            self.spawn_position = self.config.get("mothership")["spawn_right_position"]
        else:
            self.direction = 1
            self.spawn_position = self.config.get("mothership")["spawn_left_position"]

    def spawn(self):
        self.spawned = True
        self.set_spawn_direction()
        print("Spawning mothership")
        self.mothership_group.add(
            Mothership(self.spawn_position, self.direction, self.points_table)
        )
