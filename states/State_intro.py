from classes.System import System


class StateIntro:
    def __init__(self):
        self.system = System.get_instance()
        # at this point there is no concept of state machine
        print("initialised state intro")
        self.state = {}

    # inject functions rather than whole statemachine
    # maybe inject
    def enter(self, state_machine):
        self.state['invaders_moving'] = True
        self.state_machine = state_machine
        self.invader_controller = self.system.get_controller("Invader")
        self.input_controller = self.system.get_controller("Input")
        self.shield_controller = self.system.get_controller("Shield")

        # code that should run when entering this state
        self.system.add_listener("escape_button_pressed", self.on_escape_button_pressed)
        # self.system.add_listener("invader_hit", on_invader_hit)
        # def on_invader_hit() self.invader_controller....

        self.system.register_callback("get_invaders",  self.invader_controller.get_invaders)
        
        self.system.debug_callbacks()
        get_invaders_callback = self.system.get_callback("get_invaders")
        #print(get_invaders_callback)

        print("entered state intro state")

    def update(self, events):
        self.input_controller.update(events, self.state)
        self.invader_controller.update(events, self.state),
        self.shield_controller.update(events, self.state),

    def get_surfaces(self):
        return [
            self.invader_controller.get_surface(),
            self.shield_controller.get_surface(),
        ]

    def on_escape_button_pressed(self, data):
        print("escape caught in state intro")
        self.exit("GAME_START")

    def exit(self, next_state):
        self.system.remove_listener(
            "escape_button_pressed", self.on_escape_button_pressed
        )
        self.state_machine.change_to(next_state)
