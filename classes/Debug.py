import pygame, os

font = pygame.font.Font(
    os.path.join(os.path.dirname(__file__), "space_invaders.ttf"), 8
)


class Debug:
    def __init__(self):
        self.debug_requests = []

    def clear_requests(self):
        self.debug_requests = []

    def add_request(self, x, y, text):
        self.debug_requests.append((x, y, text))

    def get_requests(self):
        return self.debug_requests

    def render_requests(self, surface):
        for request in self.debug_requests:
            x, y, text = request
            debug_surf = font.render(text, False, "White")
            debug_rect = debug_surf.get_rect(topleft=(x, y))
            surface.blit(debug_surf, debug_rect)
