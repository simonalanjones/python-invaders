from classes.invader.Invader_factory import InvaderFactory
from classes.invader.Invader_container import InvaderContainer


class InvaderController:
    def __init__(self, config):
        invader_factory = InvaderFactory(config)
        self.invader_generator = invader_factory.create_invader_swarm()
        self.invader_container = InvaderContainer(config)
        self.is_moving = False
        self.swarm_complete = False
        self.countdown = 0

    def generate_next_invader(self):
        try:
            self.invader_container.add_invader(next(self.invader_generator))
        except StopIteration:
            if self.swarm_complete == False:
                self.swarm_complete = True
                self.is_moving = True
                # callback to game controller
                self.notify_swarm_complete()

    def notify_swarm_complete(self, callback):
        self.notify_swarm_complete = callback

    def pause_player_missile(self, callback):
        self.pause_player_missile = callback

    def resume_player_missile(self, callback):
        self.resume_player_missile = callback

    def get_invaders(self):
        return self.invader_container.get_invaders()

    def stop_movement(self):
        self.is_moving = False

    def start_movement(self):
        self.is_moving = True

    def check_has_landed():
        pass

    def destroy_invader_callback(self, invader):
        self.stop_movement()
        # pause invaders 1/4 second (60/15)
        self.countdown = 15
        # callback to pause player firing
        self.pause_player_missile()
        invader.explode()

    def release_non_active(self):
        self.invader_container.remove_inactive()
        self.start_movement()
        self.resume_player_missile()

    def update(self):
        if not self.swarm_complete:
            # print("generating")
            self.generate_next_invader()

        else:
            if self.countdown > 0:
                self.countdown -= 1
                if self.countdown <= 0:
                    self.release_non_active()

            if self.is_moving:
                self.invader_container.update()

        return self.invader_container
