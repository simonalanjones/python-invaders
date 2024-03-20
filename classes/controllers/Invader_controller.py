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
        self.player_is_exploding = False

        self.event_manager.add_listener(
            "entered_state_game_playing", self.on_game_playing
        )
        self.event_manager.add_listener("invader_hit", self.on_invader_hit)
        self.event_manager.add_listener("player_explodes", self.on_player_explodes)
        self.event_manager.add_listener("invaders_landed", self.on_pause_movement)

    def get_surface(self):
        return self.invader_container

    def game_restart(self):
        invader_factory = InvaderFactory()
        self.invader_generator = invader_factory.create_invader_swarm()
        self.invader_container = InvaderContainer()
        self.is_moving = False
        self.swarm_complete = False
        self.countdown = 0

    def on_game_playing(self, data):
        self.player_is_exploding = False
        self.is_moving = True

    def on_player_explodes(self, data):
        self.player_is_exploding = True
        self.is_moving = False

    def on_invader_hit(self, invader):
        self.is_moving = False
        # pause invaders 1/4 second (60/15)
        self.countdown = 15
        invader.explode()
        self.event_manager.notify("points_awarded", invader.points)

    def on_pause_movement(self, data):
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

    def release_non_active(self):
        self.invader_container.remove_inactive()
        self.event_manager.notify("invader_removed")
        if not self.player_is_exploding:
            self.is_moving = True

    def update(self, events, dt=0):
        if self.swarm_complete:
            if self.countdown > 0:
                self.countdown -= 1
                if self.countdown <= 0:
                    self.release_non_active()

            if self.is_moving:
                self.invader_container.update()

        else:
            self.generate_next_invader()

        return self.invader_container
