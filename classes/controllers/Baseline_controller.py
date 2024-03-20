from lib.Controller import Controller
from classes.containers.Baseline_container import BaselineContainer
from classes.models.Baseline import Baseline


class BaselineController(Controller):

    def __init__(self):
        super().__init__()
        self.baseline = Baseline()
        self.baseline_container = BaselineContainer()
        self.baseline_container.add(self.baseline)

    def get_surface(self):
        return self.baseline_container

    def update(self, events, dt=0):
        self.baseline_container.update()
