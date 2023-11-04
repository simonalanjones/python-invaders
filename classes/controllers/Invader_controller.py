from lib.Controller import Controller
from classes.factories.Invader_factory import InvaderFactory
from classes.containers.Invader_container import InvaderContainer


class InvaderController(Controller):
    def __init__(self):
        super().__init__()

        invader_factory = InvaderFactory()
        self.invader_generator = invader_factory.create_invader_swarm()
        self.invader_container = InvaderContainer()
        self.is_moving = False
        self.swarm_complete = False
        self.countdown = 0

        self.event_manager.add_listener("invader_hit", self.on_invader_hit)
        self.event_manager.add_listener("player_explodes", self.on_player_explodes)
        self.event_manager.add_listener("play_delay_complete", self.on_player_ready)

        self.register_callback(
            "get_invaders", lambda: self.invader_container.get_invaders()
        )

        self.register_callback(
            "get_invaders_with_clear_path",
            lambda: self.invader_container.get_invaders_with_clear_path(),
        )

        self.register_callback(
            "get_invader_count", lambda: len(self.invader_container.get_invaders())
        )

        self.register_callback(
            "get_lowest_invader_y",
            lambda: self.invader_container.get_invaders()[0].rect.y,
        )

    def game_restart(self):
        invader_factory = InvaderFactory()
        self.invader_generator = invader_factory.create_invader_swarm()
        self.invader_container = InvaderContainer()
        self.is_moving = False
        self.swarm_complete = False
        self.countdown = 0

    def on_invader_hit(self, invader):
        self.is_moving = False
        # pause invaders 1/4 second (60/15)
        self.countdown = 15
        invader.explode()
        self.event_manager.notify("points_awarded", invader.points)

    def on_player_explodes(self, data):
        self.is_moving = False

    def on_player_ready(self, data):
        self.is_moving = True

    def generate_next_invader(self):
        try:
            self.invader_container.add_invader(next(self.invader_generator))
        except StopIteration:
            if self.swarm_complete == False:
                self.swarm_complete = True
                self.is_moving = True
                self.event_manager.notify("swarm_complete")

    def check_has_landed():
        pass

    def release_non_active(self):
        self.invader_container.remove_inactive()
        self.is_moving = True
        self.event_manager.notify("invader_removed")

    def update(self, events, dt):
        if not self.swarm_complete:
            self.generate_next_invader()
        else:
            if self.countdown > 0:
                self.countdown -= 1
                if self.countdown <= 0:
                    self.release_non_active()

            if self.is_moving:
                self.invader_container.update()

        return self.invader_container
