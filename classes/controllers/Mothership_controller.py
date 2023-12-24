import pygame
from lib.Controller import Controller
from classes.models.Mothership import Mothership
from classes.config.Mothership_config import MothershipConfig
from lib.Sprite_sheet import MothershipSpriteSheet


class MothershipController(Controller):
    def __init__(self):
        super().__init__()
        self.config = MothershipConfig()
        self.sprite_sheet = MothershipSpriteSheet()
        self.cycles_until_spawn = self.config.get("cycles_until_spawn")
        self.spawn_right_position = self.config.get("spawn_right_position")
        self.spawn_left_position = self.config.get("spawn_left_position")
        self.qualifying_invader_y_position = self.config.get(
            "qualifying_invader_y_position"
        )
        self.points_table = self.config.get("points_table")
        self.mothership_image = self.sprite_sheet.get_sprite("mothership_frame")
        self.explode_image = self.sprite_sheet.get_sprite("explode_frame")
        self.player_ready = False

        # set-up non-config related variables
        self.cycles_lapsed = 0
        self.spawned = False
        self.shot_counter = 0

        self.register_callback("mothership_is_exploding", self.mothership_is_exploding)
        self.event_manager.add_listener("player_explodes", self.on_player_explodes)
        self.event_manager.add_listener("play_delay_complete", self.on_player_ready)

        self.event_manager.add_listener(
            "fire_button_pressed", self.on_update_shot_counter
        )

        # mothership sprite stored in sprite group
        self.mothership_group = pygame.sprite.Group()

    def mothership_is_exploding(self):
        if not self.mothership_group.sprites():
            return False
        if self.mothership_group.sprites()[0].active == False:
            return True

    def update(self, events, state):
        if not self.spawned:
            self.update_spawn_logic()
        else:
            return self.update_mothership(dt)

    def update_mothership(self, dt):
        if self.mothership_group.sprites():
            self.check_missile_collision()
            mothership = self.mothership_group.sprites()[0]
            return mothership.update(self.shot_counter, dt)

        # If there are no motherships in the group, reset the spawn state.
        self.reset_spawn_state()
        self.event_manager.notify("mothership_exit")

    def update_spawn_logic(self):
        if not self.check_invader_criteria() or not self.check_player_criteria():
            return False

        self.cycles_lapsed += 1
        if self.cycles_lapsed == self.cycles_until_spawn:
            self.spawn()

    def check_missile_collision(self):
        missile_callback = self.get_callback("get_player_missile")
        missile = missile_callback()
        mothership = self.mothership_group.sprites()
        if missile is not None and missile.active:
            collided = pygame.sprite.spritecollide(missile, mothership, False)
            if collided:
                self.mothership_hit()
                missile.remove()

    def mothership_hit(self):
        mothership = self.mothership_group.sprites()[0]
        points = mothership.calculate_points()

        text_surface_callback = self.get_callback("get_score_text")
        points_surface = text_surface_callback(str(points))

        mothership.explode(points_surface)
        self.event_manager.notify("mothership_hit", points)

    def reset_spawn_state(self):
        self.shot_counter = 0
        self.cycles_lapsed = 0
        self.spawned = False

    def on_player_explodes(self, data):
        self.player_ready = False

    def on_player_ready(self, data):
        self.player_ready = True

    def on_update_shot_counter(self, data):
        self.shot_counter = (self.shot_counter + 1) % 16

    def check_player_criteria(self):
        return self.player_ready

    def check_invader_criteria(self):
        invader_count = self.get_callback("get_invader_count")()
        lowest_invader_y = self.get_callback("get_lowest_invader_y")()

        return (
            invader_count >= 8
            and lowest_invader_y >= self.qualifying_invader_y_position
        )

    def get_spawn_direction(self):
        return -1 if self.shot_counter % 2 == 1 else 1

    def get_spawn_position(self):
        return (
            self.spawn_right_position
            if self.shot_counter % 2 == 1
            else self.spawn_left_position
        )

    def spawn(self):
        self.event_manager.notify("mothership_spawned")
        self.spawned = True
        self.mothership_group.add(
            Mothership(
                self.mothership_image,
                self.explode_image,
                self.get_spawn_position(),
                self.get_spawn_direction(),
                self.points_table,
            )
        )
