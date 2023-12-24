from classes.System import System

# hold all game state here for all controllers to use
# allow controllers to access state related to other controllers?
# create a basic state class which has common functions
class StateGameStarts:
    def __init__(self):
        self.system = System.get_instance()

        # we'll pass the state array to all controllers so they can share the state
        # and we'll allow controllers to update the state back up
        self.state = {
            'invaders_moving': True,
            'is_moving_left': False,
            'is_moving_right': False,
            'fire_button_pressed': False,
            'player_enabled': True,
            'bombs_enabled': True,
        }

        # self.state = {
        #     'invaders_moving': False,
        #     'is_moving_left': False,
        #     'is_moving_right': False,
        #
        #     'fire_button_pressed': {
        #           'default': False,#needed if reseting use default
        #           'one_shot': True,
        #           'value': False
        #      }
        # }
        
        print("initialised state game")

    def reset_state(self, index):
        pass
        # this would return the state identified by index back to its reset value

    def update_state(returned_state):
        self.state = returned_state

    # update to be able to specify 'one shot' = True
    # could reset on subsequent passes
    ### maybe even store previous value ####
    def set_state(self, index, value):
        self.state[index] = value

    def get_state_value(self, index):
        if index in self.state:
            return self.state[index]


    def enter(self, state_machine):
        self.state_machine = state_machine

        self.invader_controller = self.system.get_controller("Invader")
        self.input_controller = self.system.get_controller("Input")
        self.shield_controller = self.system.get_controller("Shield")
        self.bomb_controller = self.system.get_controller("Bomb")
        self.player_controller = self.system.get_controller("Player")
        self.player_missile_controller = self.system.get_controller("PlayerMissile")


        self.bomb_controller.enabled = True
        self.player_controller.spawn_player()
        self.player_missile_controller.ready_flag = True

        #self.system.add_listener("player_explodes", self.on_player_hit)
        self.system.add_listener("invader_hit", self.invader_controller.on_invader_hit)
        

        #player events
        self.system.add_listener("left_button_pressed", self.on_move_left)
        self.system.add_listener("left_button_released", self.on_move_left_exit)
        self.system.add_listener("right_button_pressed", self.on_move_right)
        self.system.add_listener("right_button_released", self.on_move_right_exit)
        self.system.add_listener("fire_button_pressed", self.on_fire_pressed)
        
        #self.system.register_callback("get_player", self.player_controller.get_player)

        self.player_missile_controller.get_player_callback = self.player_controller.get_player
        self.player_missile_controller.get_invaders_callback = self.invader_controller.get_invaders

        self.bomb_controller.get_invaders_callback = self.invader_controller.get_invaders
        self.bomb_controller.get_player_callback = self.player_controller.get_player
        self.bomb_controller.get_invaders_clearpath_callback = self.invader_controller.invader_container.get_invaders_with_clear_path

        self.shield_controller.get_invaders_callback = self.invader_controller.get_invaders
        self.shield_controller.get_bombs_callback = self.bomb_controller.get_bombs

        self.shield_controller.get_player_missile_callback = self.player_missile_controller.get_player_missile

        print(self.shield_controller.get_player_missile_callback)


        #self.system.register_callback("get_invaders",  self.invader_controller.get_invaders)
        #self.system.register_callback("get_invaders_with_clear_path",  lambda: self.invader_controller.invader_container.get_invaders_with_clear_path())
        #self.system.register_callback("get_lowest_invader_y", lambda: self.invader_controller.invader_container.get_invaders()[0].rect.y)
        #self.system.register_callback("get_invader_count", lambda: len(self.invader_controller.invader_container.get_invaders()))

        

    # have a function that sets state on a index of the dict and specify whether it clears or changes on subsequent updates

    def on_fire_pressed(self, data):
        self.set_state('fire_button_pressed', True)

    def on_move_left(self, data):
        self.set_state('is_moving_left', True)

    def on_move_left_exit(self, data):
        self.set_state('is_moving_left', False)

    def on_move_right(self, data):
        self.set_state('is_moving_right', True)

    def on_move_right_exit(self, data):
        self.set_state('is_moving_right', False)

    def on_fire_button_pressed(self, data):
        print("fire button caught in state game starts")
        self.exit("GAME_INTRO")

    def on_player_hit(self, data):
        print("player was hit")
        #self.exit("PLAYER_EXPLODING")

    def update(self, events):
        self.input_controller.update(events, self.state)
        self.invader_controller.update(events, self.state)
        self.shield_controller.update(events, self.state)
        self.bomb_controller.update(events, self.state)
        self.player_controller.update(events, self.state)
        self.player_missile_controller.update(events, self.state)
        self.set_state('fire_button_pressed', False)

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
