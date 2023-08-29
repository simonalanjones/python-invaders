from classes.Controller import Controller
from classes.invader.Invader_factory import InvaderFactory
from classes.invader.Invader_container import InvaderContainer


class InvaderController(Controller):
    def __init__(self, config):
        super().__init__(config)
        invader_factory = InvaderFactory(config)
        self.invader_generator = invader_factory.create_invader_swarm()
        self.invader_container = InvaderContainer(config)
        self.is_moving = False
        self.swarm_complete = False
        self.countdown = 0

        # callbacks defined in Game_controller
        self.pause_player_missile_callback = None
        self.resume_player_missile_callback = None

    def generate_next_invader(self):
        try:
            self.invader_container.add_invader(next(self.invader_generator))
        except StopIteration:
            if self.swarm_complete == False:
                self.swarm_complete = True
                self.is_moving = True
                self.event_manager.notify("swarm_complete")

    def get_invaders(self):
        return self.invader_container.get_invaders()

    def stop_movement(self):
        self.is_moving = False

    def start_movement(self):
        self.is_moving = True

    def check_has_landed():
        pass

    def on_f1_pressed(self, stuff):
        invaders = self.get_invaders()
        print("start of y")
        for invader in invaders:
            invader.print_y()
        print("end of y")

    def on_invader_hit(self, invader):
        self.stop_movement()
        # # pause invaders 1/4 second (60/15)
        self.countdown = 15
        invader.explode()
        self.event_manager.notify("points_awarded", invader.points)

    def release_non_active(self):
        self.invader_container.remove_inactive()
        self.start_movement()
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
