import pygame
from sys import exit as sys_exit


class EndingScreen:
    """Displays an ending screen with restart and exit buttons."""

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (100, 100, 100)
    LIGHT_GREY = (180, 180, 180)

    ENDING_MESSAGES = {
        "bad": "You Lost! Try Again.",
        "good": "Good Job! But not all enemies were slain...",
        "true": "Congratulations! The True Ending is yours!"
    }

    def __init__(self, screen: pygame.Surface, screen_size: tuple[int, int]) -> None:
        self._screen = screen
        self._screen_size = screen_size
        self._clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 36)

        # Button setup
        self.button_width = 180
        self.button_height = 60
        center_x = screen_size[0] // 2

        self.restart_button_rect = pygame.Rect(center_x - self.button_width - 20, screen_size[1] // 2 + 100,
                                               self.button_width, self.button_height)
        self.exit_button_rect = pygame.Rect(center_x + 20, screen_size[1] // 2 + 100,
                                            self.button_width, self.button_height)

    def draw_button(self, rect: pygame.Rect, text: str, hover: bool = False):
        """Draws a button with text."""
        color = self.LIGHT_GREY if hover else self.GREY
        pygame.draw.rect(self._screen, color, rect, border_radius=15)
        pygame.draw.rect(self._screen, self.WHITE, rect, width=2, border_radius=15)
        label = self.small_font.render(text, True, self.WHITE)
        label_rect = label.get_rect(center=rect.center)
        self._screen.blit(label, label_rect)

    def show(self, ending_type: str) -> None:
        """Display the appropriate ending and wait for user action."""
        text = self.ENDING_MESSAGES.get(ending_type, "Unknown Ending")

        running = True
        while running:
            self._screen.fill(self.BLACK)

            # Render main message
            msg_surface = self.font.render(text, True, self.WHITE)
            msg_rect = msg_surface.get_rect(center=(self._screen_size[0] // 2, self._screen_size[1] // 2 - 50))
            self._screen.blit(msg_surface, msg_rect)

            # Get mouse position and check hover states
            mouse_pos = pygame.mouse.get_pos()
            restart_hover = self.restart_button_rect.collidepoint(mouse_pos)
            exit_hover = self.exit_button_rect.collidepoint(mouse_pos)

            # Draw buttons
            self.draw_button(self.restart_button_rect, "Restart", restart_hover)
            self.draw_button(self.exit_button_rect, "Exit", exit_hover)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys_exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.restart_button_rect.collidepoint(event.pos):
                        from main import main  # local import avoids circular import
                        main()
                    elif self.exit_button_rect.collidepoint(event.pos):
                        sys_exit()

            self._clock.tick(30)