from lib.Controller import Controller
from classes.config.Mothership_config import MothershipConfig
from classes.containers.Mothership_container import MothershipContainer


class MothershipController(Controller):
    def __init__(self):
        super().__init__()
        self.mothership_container = MothershipContainer()

        self.config = MothershipConfig()
        self.cycles_until_spawn = self.config.get("cycles_until_spawn")

        self.qualifying_invader_y_position = self.config.get(
            "qualifying_invader_y_position"
        )

        self.player_ready = False

        # set-up non-config related variables
        self.cycles_lapsed = 0
        self.spawned = False

        self.callback_manager.register_callback(
            "mothership_is_exploding", self.mothership_is_exploding
        )
        self.event_manager.add_listener("player_explodes", self.on_player_explodes)
        self.event_manager.add_listener("play_delay_complete", self.on_player_ready)
        self.event_manager.add_listener("mothership_exit", self.on_mothership_exit)

    def get_surface(self):
        return self.mothership_container

    def mothership_is_exploding(self):
        if not self.mothership_container.sprite:
            return False
        if self.mothership_container.sprite.active == False:
            return True

    def update(self, events, dt=0):
        if not self.mothership_container.sprite:
            self.update_spawn_logic()
        else:
            self.mothership_container.update()
            # return self.update_mothership(dt)

    # update shot count
    # def update_mothership(self, dt):
    #     print("here")
    #     if self.mothership_container.sprite:
    #         mothership = self.mothership_container.sprite
    #         return mothership.update(self.shot_counter, dt)

    #     # If there are no motherships in the group, reset the spawn state.
    #     self.reset_spawn_state()
    #     self.event_manager.notify("mothership_exit")

    def update_spawn_logic(self):
        # ********** keep this **************
        # if not self.check_invader_criteria() or not self.check_player_criteria():
        #     return False

        self.cycles_lapsed += 1
        if self.cycles_lapsed == self.cycles_until_spawn:
            self.mothership_container.spawn()

    # set up a sprite group in the container
    # def check_missile_collision(self):
    #     return
    #     missile_callback = self.get_callback("get_player_missile")
    #     missile = missile_callback()
    #     mothership = self.mothership_group.sprites()
    #     if missile is not None and missile.active:
    #         collided = pygame.sprite.spritecollide(missile, mothership, False)
    #         if collided:
    #             self.mothership_hit()
    #             missile.remove()

    # def mothership_hit(self):
    #     mothership = self.mothership_group.sprites()[0]
    #     points = mothership.calculate_points()

    #     text_surface_callback = self.get_callback("get_score_text")
    #     points_surface = text_surface_callback(str(points))

    #     mothership.explode(points_surface)
    #     self.event_manager.notify("mothership_hit", points)

    def reset_spawn_state(self):
        self.cycles_lapsed = 0
        self.spawned = False

    def on_player_explodes(self, data):
        self.player_ready = False

    def on_player_ready(self, data):
        self.player_ready = True

    def on_mothership_exit(self, data):
        self.reset_spawn_state()

    def check_player_criteria(self):
        return self.player_ready

    def check_invader_criteria(self):
        invader_count = self.callback_manager.callback("get_invader_count")
        lowest_invader_y = self.callback_manager.callback("get_lowest_invader_y")

        return (
            invader_count
            >= 8
            # and lowest_invader_y >= self.qualifying_invader_y_position
        )

    def get_spawn_direction(self):
        return -1 if self.shot_counter % 2 == 1 else 1

    def get_spawn_position(self):
        return (
            self.spawn_right_position
            if self.shot_counter % 2 == 1
            else self.spawn_left_position
        )

    # def spawn(self):
    #     print("spawned ms")
    #     self.event_manager.notify("mothership_spawned")
    #     self.spawned = True
    #     self.mothership_container.add(
    #         Mothership(
    #             self.mothership_image,
    #             self.explode_image,
    #             self.get_spawn_position(),
    #             self.get_spawn_direction(),
    #             self.points_table,
    #         )
    #     )
