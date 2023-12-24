from lib.Controller import Controller
from classes.factories.Invader_factory import InvaderFactory
from classes.containers.Invader_container import InvaderContainer


class InvaderController(Controller):
    def __init__(self):
        super().__init__()

        self.state = {}

        invader_factory = InvaderFactory()
        self.invader_generator = invader_factory.create_invader_swarm()
        self.invader_container = InvaderContainer()
        self.swarm_complete = False
        self.countdown = 0

        

        # can we do this outside of the controller like in the state
        # suppose we follow the react method of having access to state setting,
        #self.event_manager.add_listener("invader_hit", self.on_invader_hit)
        #self.event_manager.add_listener("player_explodes", self.on_player_explodes)
        self.event_manager.add_listener("play_delay_complete", self.on_player_ready)

        # self.register_callback(
        #     "get_invaders", lambda: self.invader_container.get_invaders()
        # )

        # self.register_callback(
        #     "get_invaders_with_clear_path",
        #     lambda: self.invader_container.get_invaders_with_clear_path(),
        # )

        # self.register_callback(
        #     "get_invader_count", lambda: len(self.invader_container.get_invaders())
        # )

        # self.register_callback(
        #     "get_lowest_invader_y",
        #     lambda: self.invader_container.get_invaders()[0].rect.y,
        # )

    # maybe this could be in base controller
    # injects functions that can get state and change state
    def set_up_state(self, fn_state_change, fn_get_state):
        pass


    # should this be in the state rather than controller
    # this isn't core functionality and appears to be controlling state of vars
    def game_restart(self):
        invader_factory = InvaderFactory()
        self.invader_generator = invader_factory.create_invader_swarm()
        self.invader_container = InvaderContainer()
        self.is_moving = False
        self.swarm_complete = False
        self.countdown = 0

    def get_invaders(self):
        return self.invader_container.get_invaders()
    # suppose we get vars like coundown from the state object
    # and vars like is_moving
    # function get state set state
    # like in react
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

    def get_surface(self):
        return self.invader_container

    # have another function that receives state?
    def update(self, events, state):
        self.state = state
        self.is_moving = state['invaders_moving']
        if not self.swarm_complete:
            self.generate_next_invader()
        else:
            if self.countdown > 0:
                self.countdown -= 1
                if self.countdown <= 0:
                    self.release_non_active()

            if self.is_moving:
                self.invader_container.update()
