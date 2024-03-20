import pygame
import itertools
from lib.Event_manager import EventManager


class Collision:
    def __init__(self, sprite1, sprite2, collision_area):
        self.sprites = (sprite1, sprite2)
        self.collision_area = collision_area

    def extract_sprite_by_class(self, target_class):
        for sprite in self.sprites:
            if sprite.__class__.__name__ == target_class:
                return sprite
        return None

    def collision_area(self):
        return self.collision_area

    def overlap_area(self):
        return self.collision_area.overlap_area


class CollisionManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = CollisionManager()
        return cls._instance

    def __init__(self):
        self.grouped_containers = {}
        self.event_manager = EventManager.get_instance()

    # when registering, you could specify whether to use masks or rects and use different collision methods
    # to allow for precise or fast
    # perhaps sprites in group could specify their own collision rect and
    # also have a debug mode on the sprite which shows it's collision rect if used
    # https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.groupcollide
    def register_group(
        self, name, function, collision_group=None, callback=None, autorun=False
    ):
        if collision_group not in self.grouped_containers:
            self.grouped_containers[collision_group] = []
        self.grouped_containers[collision_group].append(
            (name, function, callback, autorun)
        )

    ############################### new code ########################

    def run_autorun_groups(self):
        for collision_group, containers in self.grouped_containers.items():

            for name, function, callback, autorun in containers:
                if autorun:
                    # print(collision_group)
                    self.check_collisions(collision_group)

    def check_collisions(self, collision_group):
        containers_to_check = self.get_containers_to_check(collision_group)
        unique_pairs = self.get_unique_pairs(containers_to_check)

        for pair in unique_pairs:
            container1_name, container1_function, callback1, autorun1 = pair[0]
            container2_name, container2_function, callback2, autorun2 = pair[1]

            self.check_collision_between_groups(
                container1_function, container2_function, callback1, callback2
            )

    def get_containers_to_check(self, collision_group):
        if collision_group is not None and collision_group in self.grouped_containers:
            return self.grouped_containers[collision_group]
        else:
            return [
                (name, function, callback)
                for group in self.grouped_containers.values()
                for name, function, callback in group
            ]

    def get_unique_pairs(self, containers_to_check):
        return itertools.combinations(containers_to_check, 2)

    def check_collision_between_groups(
        self, container1_function, container2_function, callback1, callback2
    ):
        container1_group = container1_function()
        container2_group = container2_function()

        if (
            container1_group
            and container2_group
            and hasattr(container1_group, "__iter__")
            and hasattr(container2_group, "__iter__")
        ):
            self.check_collision_between_sprites(
                container1_group, container2_group, callback1, callback2
            )

    def check_collision_between_sprites(
        self, container1_group, container2_group, callback1, callback2
    ):
        for sprite1 in container1_group:
            for sprite2 in container2_group:
                collision_area = pygame.sprite.collide_mask(sprite1, sprite2)
                if collision_area is not None:
                    self.handle_collision_event(
                        sprite1, sprite2, collision_area, callback1, callback2
                    )

    def handle_collision_event(
        self, sprite1, sprite2, collision_area, callback1, callback2
    ):
        self.event_manager.notify(
            f"{sprite1.__class__.__name__}_{sprite2.__class__.__name__}_collision",
            [sprite1, sprite2, collision_area],
        )
        if callback1 is not None:
            callback1(Collision(sprite1, sprite2, collision_area))
        if callback2 is not None:
            callback2(Collision(sprite1, sprite2, collision_area))

    ##################### end new code ###################

    # original check_collisions
    def ___check_collisions(self, collision_group):
        containers_to_check = []
        for group in self.grouped_containers.values():
            for name, function, callback, autorun in group:
                containers_to_check.append((name, function, callback))

        # Use itertools.combinations to get unique pairs
        unique_pairs = list(itertools.combinations(containers_to_check, 2))
        # print(f"Number of unique pairs to check: {len(unique_pairs)}")

        for (container1_name, container1_function, callback1), (
            container2_name,
            container2_function,
            callback2,
        ) in unique_pairs:
            container1_group = container1_function()
            container2_group = container2_function()

            # Check both groups are not empty and are iterable
            if (
                container1_group
                and container2_group
                and hasattr(container1_group, "__iter__")
                and hasattr(container2_group, "__iter__")
            ):
                # print(
                #     f"Checking collisions between {container1_name} and {container2_name}"
                # )
                # print(
                #     f"Number of sprites in {container1_name}: {len(container1_group)}"
                # )
                # print(
                #     f"Number of sprites in {container2_name}: {len(container2_group)}"
                # )
                # Iterate through sprites in both containers
                for sprite1 in container1_group:
                    for sprite2 in container2_group:
                        # Perform collision detection using sprite masks
                        collision_area = pygame.sprite.collide_mask(sprite1, sprite2)
                        if collision_area is not None:
                            # print("Collision detected!")
                            # event notification
                            self.event_manager.notify(
                                f"{sprite1.__class__.__name__}_{sprite2.__class__.__name__}_collision",
                                [sprite1, sprite2, collision_area],
                            )
                            # fire callback if specified
                            if callback1 is not None:
                                callback1(Collision(sprite1, sprite2, collision_area))
                            if callback2 is not None:
                                callback2(Collision(sprite1, sprite2, collision_area))

                            # default action is to return a Collision object
                            return Collision(sprite1, sprite2, collision_area)

        # Return None if no collision is detected
        return None

    def debug(self):
        print("===== CollisionManager Debug =====")
        for collision_group, containers in self.grouped_containers.items():
            print(f"Collision Group: {collision_group}")
            for name, function, _, _ in containers:
                print(f"  - Container: {name}")
                if callable(function):
                    container_result = function()
                    if container_result is not None:
                        num_sprites = len(container_result)
                        print(f"  - Number of Sprites: {num_sprites}")
                    else:
                        print("  - Number of Sprites: Container result is None")
                else:
                    print(
                        "  - Number of Sprites: Unable to determine (function not callable)"
                    )
        print("=================================")

    def __debug(self):
        print("===== CollisionManager Debug =====")
        for collision_group, containers in self.grouped_containers.items():
            print(f"Collision Group: {collision_group}")
            for name, function in containers:
                print(f"  - Container: {name}")
                if callable(function):
                    num_sprites = len(function())
                    print(f"  - Number of Sprites: {num_sprites}")
                else:
                    print(
                        "  - Number of Sprites: Unable to determine (function not callable)"
                    )

                # num_sprites = len(function())
                # print(f"  - Number of Sprites: {num_sprites}")
            print("=================================")
