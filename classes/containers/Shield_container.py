from lib.Container import Container


class ShieldContainer(Container):
    def __init__(self):
        super().__init__()

        self.collision_manager.register_group(
            name="shield_collisions",
            function=self.sprites,
            collision_group="shield_collisions",
            callback=self.on_collision,
        )

    def update(self):
        self.collision_manager.check_collisions("shield_collisions")

    def on_collision(self, collision):
        bomb_sprite = collision.extract_sprite_by_class("Bomb")
        shield_sprite = collision.extract_sprite_by_class("Shield")
        missile_sprite = collision.extract_sprite_by_class("PlayerMissile")
        invader_sprite = collision.extract_sprite_by_class("Invader")

        # handle collision between invader and shield
        if shield_sprite != None and invader_sprite != None:
            shield_sprite.invader_damage(invader_sprite)

        # handle collision between player missile and shield
        if shield_sprite != None and missile_sprite != None and missile_sprite.active:

            # missile_sprite.explode()
            self.callback_manager.callback("explode_player_missile")

            shield_sprite.missile_damage(
                missile_sprite
            )  # need to remove where the missile collided too
            # self.event_manager.notify("pause_pressed")
            # return
            self.callback_manager.callback("remove_player_missile")

        # handle collision between invader bomb and shield
        if shield_sprite != None and bomb_sprite != None and bomb_sprite.active:
            bomb_sprite.explode()
            shield_sprite.bomb_collision(bomb_sprite)

    def get_shields(self):
        return self.sprites()
