from classes.Event_manager import EventManager


class Controller:
    def __init__(self, config):
        self.event_manager = EventManager.get_instance()
        self.config = config
