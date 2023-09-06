class EventManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = EventManager()
        return cls._instance

    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def remove_listener(self, event_type, listener):
        if event_type in self.listeners:
            self.listeners[event_type].remove(listener)

    def notify(self, event_type, data=None):
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(data)
