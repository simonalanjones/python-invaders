from classes.System import System


class StatePlayerExploding:
    def __init__(self):
        self.system = System.get_instance()

        self.state = {
            'invaders_moving': False,
        }

        print("initialised state StatePlayerExploding")
        # self.event_manager.add_listener(
        #     "player_explosion_complete", self.on_player_explosion_complete
        # )

    def set_state(self, index, value):
        self.state[index] = value

    def get_state_value(self, index):
        if index in self.state:
            return self.state[index]    

    def enter(self, state_machine):
        print("entered player explode state")
        self.state_machine = state_machine

        self.invader_controller = self.system.get_controller("Invader")
        self.shield_controller = self.system.get_controller("Shield")
        self.bomb_controller = self.system.get_controller("Bomb")
        self.player_controller = self.system.get_controller("Player")
        self.player_missile_controller = self.system.get_controller("PlayerMissile")

        self.bomb_controller.enabled = False
        self.player_controller.explode_player()
        #self.player_missile_controller.get_player_callback = self.player_controller.get_player

    def on_player_explosion_complete(self, data):
        print("in state explode - animation complete")

    def update(self, events):
        self.invader_controller.update(events, self.state)
        self.shield_controller.update(events, self.state)
        self.bomb_controller.update(events, self.state)
        self.player_controller.update(events, self.state)
        self.player_missile_controller.update(events, self.state)

    # use array and look for method on controller get_surface
    def get_surfaces(self):
        return [
            self.player_missile_controller.get_surface(),
            self.invader_controller.get_surface(),
            self.shield_controller.get_surface(),
            self.bomb_controller.get_surface(),
            self.player_controller.get_surface(),
        ]


    def exit(self, next_state):
        self.state_machine.change_to(next_state)
