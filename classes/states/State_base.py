from lib.Event_object import Event_object


class StateBase(Event_object):
    def __init__(self):
        super().__init__()
        self.state_name = self._state_name(self.__class__.__name__)
        self.debug = False
        self.change_to = None
        self.registered_listeners = {}
        self.controllers = []
        self._debug(f"Initialised state: {self.state_name}")

    def enter(self, change_to):
        self._debug(f"Entered state: {self.state_name}")
        self.event_manager.notify("entered_" + self.state_name)
        self.change_to = change_to

    # child states will have their update method called
    def update(self, events):
        pass

    def notify(self, event_type, data=None):
        self.event_manager.notify(event_type, data)

    def add_listener(self, event_type, listener):
        if event_type not in self.registered_listeners:
            self.registered_listeners[event_type] = []
        self.registered_listeners[event_type].append(listener)
        self.event_manager.add_listener(event_type, listener)
        self._debug(f"Adding event {event_type} from  {listener}")

    def exit(self, next_state):
        self._debug(f"Exiting state: {self.state_name}")

        # Remove all listeners registered within this state
        for event_type, listeners in self.registered_listeners.items():
            for listener in listeners:
                self.event_manager.remove_listener(event_type, listener)
                self._debug(f"removing event {event_type} from  {listener}")

        self.event_manager.notify(f"exited_{self.state_name}")
        self.change_to(next_state)

    def remove_controller(self, controller_name):
        if controller_name in self.controllers:
            self.controllers.remove(controller_name)
            self._debug(f"{controller_name} removed.")
        else:
            self._debug(f"{controller_name} not found in the list.")

    def _debug(self, debug_string):
        if self.debug:
            print(debug_string)

    def _state_name(self, class_name):
        result = [class_name[0].lower()]

        for char in class_name[1:]:
            if char.isupper():
                result.extend(["_", char.lower()])
            else:
                result.append(char)

        return "".join(result)
