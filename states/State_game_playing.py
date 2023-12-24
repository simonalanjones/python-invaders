class StateGamePlaying:
    def __init__(self):
        print("initialised state playing")
        # self.state_machine = state_machine
        ## maybe load in specific controllers here?

        ## how to get controllers to indicate when the state has changed
        ## use callbacks or events?
        ## pass the statemachine/state to each controller?
        ## have the game controller receive the statemachine?

        ## give the invader_controller a hook into this code
        ## have invader_controller call a function in this state when an event happens

        # load controllers needed
        # add events betwen the controller back to the state functions
        # invader_controller.event_manager.add_listener("invader_hit", self.on_invader_hit)

    def enter(self):
        # code that should run when entering this state
        print("entered state game playing")

    def update(self):
        # code that should run every frame
        print("in update on game playing")

    def exit(self, next_state):
        self.state_machine.change_to(next_state)
