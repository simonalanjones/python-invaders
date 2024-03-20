from lib.Controller import Controller
from classes.factories.Shield_factory import ShieldFactory


class ShieldController(Controller):
    def __init__(self):
        super().__init__()
        self.rendering_order = -1
        self.shield_container = ShieldFactory().create_shields()

    def get_surface(self):
        return self.shield_container

    # place any code here that should run when controllers have loaded
    def game_ready(self):
        return

    def update(self, events, dt=0):
        self.shield_container.update()
