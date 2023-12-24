from classes.Display import Display


# idea: have system class that holds event management and controller management and display
# system has methods to delegate to above system
# then get events and controllers out of state machine
class StateMachine:
    def __init__(self, states, starting_state):
        self.display = Display()
        self.states = states
        self.state = states[starting_state]
        self.enter_state()

    def get_state_name(self):
        return self.state.name

    def change_to(self, new_state):
        self.state = self.states[new_state]
        self.enter_state()

    def update(self, events):
        self.state.update(events)
        returned_surfaces = self.state.get_surfaces()
        self.display.update(returned_surfaces)

    def enter_state(self):
        self.state.enter(self)


# extends Node

# class_name StateMachine

# signal state_bootup_entered
# signal state_crashed_entered
# signal state_demo_crashed_entered
# signal state_demo_over_entered
# signal state_demo_playing_entered
# signal state_game_over_entered
# signal state_game_over_high_scores_entered
# signal state_intro_entered
# signal state_key_controls_entered
# signal state_high_scores_entered
# signal state_player_starts
# signal state_score_table_entered
# signal state_mission_complete_entered
# signal state_playing_entered
# signal state_settings_entered
# signal state_achievements_entered


# const DEBUG = true

# var state: Object
# var mission_complete:bool = false
# var base_destroyed:bool = false
# var demo_mode: bool = false
# var crashed: bool = false
# var lives_depleted: bool = false


# func is_demo_mode() -> bool:
# 	return demo_mode


# func set_demo_mode(value: bool) -> void:
# 	demo_mode = value


# func set_player_crashed() -> void:
# 	crashed = true

# func clear_player_crashed() -> void:
# 	crashed = false


# func set_mission_completed() -> void:
# 	# set the flag in case ship is destroyed during base explosion
# 	# we want to allow for respawn and immediate exit to congrats screen
# 	mission_complete = true


# func set_base_destroyed(_points) -> void:  # signal connects with points
# 	base_destroyed = true


# func set_lives_depleted():
# 	lives_depleted = true


# func clear_lives_depleted():
# 	lives_depleted = false


# func get_state_name() -> String:
# 	return state.name


# func _ready() -> void:
# 	# important - need bootup node first to allow delay
# 	# otherwise signals do not completely load in game.gd
# 	state = get_node("State_bootup")
# 	_enter_state()


# func change_to(new_state) -> void:
# 	state = get_node(new_state)
# 	_enter_state()


# func _input(event) -> void:
# 	if state.has_method("input"):
# 		state.input(event)


# func _unhandled_key_input(event) -> void:
# 	if state.has_method("unhandled_key_input"):
# 		state.unhandled_key_input(event)


# func _process(delta) -> void:
# 	if state.has_method("process"):
# 		state.process(delta)


# func _enter_state() -> void:
# 	if DEBUG:
# 		print("Entering state: ", state.name)

# 	match state.name:
# 		"State_bootup":	emit_signal("state_bootup_entered")
# 		"State_intro": emit_signal("state_intro_entered")
# 		"State_settings": emit_signal("state_settings_entered")
# 		"State_key_controls": emit_signal("state_key_controls_entered")
# 		"State_achievements": emit_signal("state_achievements_entered")
# 		"State_high_scores": emit_signal("state_high_scores_entered")
# 		"State_score_table": emit_signal("state_score_table_entered")
# 		"State_player_starts": emit_signal("state_player_starts")
# 		"State_playing": emit_signal("state_playing_entered")
# 		"State_demo_playing": emit_signal("state_demo_playing_entered")
# 		"State_demo_crashed": emit_signal("state_demo_crashed_entered")
# 		"State_demo_over": emit_signal("state_demo_over_entered")
# 		"State_crashed": emit_signal("state_crashed_entered")
# 		"State_game_over": emit_signal("state_game_over_entered")
# 		"State_game_over_high_scores": emit_signal("state_game_over_high_scores_entered")
# 		"State_mission_complete": emit_signal("state_mission_complete_entered")

# 	# Give the new state a reference to this state machine script
# 	state.fsm = self
# 	state.enter()
