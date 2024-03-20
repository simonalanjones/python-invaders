from lib.Event_object import Event_object


class Controller(Event_object):
    def __init__(self):
        super().__init__()
        # add any extra method or properties needed for all controllers

    # simple wrapper method that proxies event manager
    def add_listener(self, event_type, listener):
        self.event_manager.add_listener(event_type, listener)

    def register_callback(self, key, callback, name=None):
        self.callback_manager.register_callback(key, callback, name)
