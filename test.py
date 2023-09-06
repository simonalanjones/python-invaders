class MyController:
    callbacks = {}  # Class-level dictionary to store callbacks

    def __init__(self):
        pass

    @classmethod
    def register_callback(cls, key, callback):
        cls.callbacks[key] = callback

    @classmethod
    def get_callback(cls, key):
        return cls.callbacks.get(key)


class ShieldController(MyController):
    def __init__(self):
        super().__init__()
        self.register_callbacks()

    def get_shields(self):
        return ["Shield1", "Shield2"]

    def get_shield_count(self):
        return 2

    def register_callbacks(self):
        self.register_callback("get_shields", self.get_shields)
        self.register_callback("get_shield_count", self.get_shield_count)

        self.get_invader_callback = self.get_callback("get_invaders")
        self.get_bombs_callback = self.get_callback("get_bombs")

    def activate_callback(self):
        print("inside shield controller")
        bomb_callback = self.get_callback("get_bombs")
        invader_callback = self.get_callback("get_invaders")

        invaders = invader_callback()
        bombs = bomb_callback()
        print(f"Invaders: {invaders}")
        print(f"Bombs: {bombs}")
        print("-----------")


class BombController(MyController):
    def __init__(self):
        super().__init__()
        self.register_callbacks()

    def get_bombs(self):
        return ["Bomb1", "Bomb2"]

    def get_bomb_count(self):
        return 2

    def register_callbacks(self):
        # Register callbacks specific to BombController
        self.register_callback("get_bombs", self.get_bombs)
        self.register_callback("get_bomb_count", self.get_bomb_count)

        self.get_invaders_callback = self.get_callback("get_invaders")
        self.get_shields_callback = self.get_callback("get_shields")

    def activate_callback(self):
        print("inside bomb controller")
        invader_callback = self.get_callback("get_invaders")
        invaders = invader_callback()
        print(f"Invaders: {invaders}")

        shield_callback = self.get_callback("get_shields")
        shields = shield_callback()
        print(f"Shields: {shields}")
        print("-------------")


class InvaderController(MyController):
    def __init__(self):
        super().__init__()
        self.register_callbacks()

    def register_callbacks(self):
        # Register callbacks specific to BombController
        self.register_callback("get_invaders", self.get_invaders)
        self.register_callback("get_invader_count", self.get_invader_count)
        self.get_bombs_callback = self.get_callback("get_bombs")

    def get_invaders(self):
        return ["Invader1", "Invader2", "Invader3"]

    def get_invader_count(self):
        return 3

    def activate_callback(self):
        print("inside invader controller")
        bomb_callback = self.get_callback("get_bombs")
        bombs = bomb_callback()
        print(f"Bombs: {bombs}")
        print("-----------")


# Create an instance of BombController
invader_controller = InvaderController()
bomb_controller = BombController()
shield_controller = ShieldController()

bomb_controller.activate_callback()
invader_controller.activate_callback()
shield_controller.activate_callback()

# Retrieve and use the "get_invaders" callback
# get_invaders_callback = invader_controller.get_callback("get_invaders")
# get_bombs_callback = bomb_controller.get_callback("get_bombs")

# if get_invaders_callback:
#     invaders = get_invaders_callback()
#     print(f"Invaders: {invaders}")
# else:
#     print("Callback not found")

# if get_bombs_callback:
#     bombs = get_bombs_callback()
#     print(f"Bombs: {bombs}")
# else:
#     print("Callback not found")
