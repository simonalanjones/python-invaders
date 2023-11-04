import pygame
import sys
import time


class GameOverAnimation:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.BACKGROUND_COLOR = (255, 255, 255)
        self.TEXT_COLOR = (0, 0, 0)
        self.FONT_SIZE = 36
        self.FONT_NAME = "Arial"
        self.game_over_text = "GAME OVER"
        self.font = pygame.font.Font(None, self.FONT_SIZE)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Game Over Animation")

    def create_text_surface(self, text):
        return self.font.render(text, True, self.TEXT_COLOR)

    def run(self):
        running = True
        current_text = ""
        char_timer = 0
        char_index = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(self.BACKGROUND_COLOR)

            if char_index < len(self.game_over_text):
                current_text += self.game_over_text[char_index]
                char_index += 1

            text_surface = self.create_text_surface(current_text)

            text_rect = text_surface.get_rect()
            text_rect.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)

            self.screen.blit(text_surface, text_rect)
            pygame.display.flip()

            if char_index < len(self.game_over_text):
                time.sleep(1)  # Wait 1 second for each character

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = GameOverAnimation()
    game.run()
