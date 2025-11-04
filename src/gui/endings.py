import pygame
from sys import exit as sys_exit


class EndingScreen:
    """Displays an ending screen with restart and exit buttons."""

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (100, 100, 100)
    LIGHT_GREY = (170, 170, 170)

    ENDING_MESSAGES = {
        "bad": "You Lost! Try Again.",
        "good": "Good Job! But not all enemies were slain...",
        "true": "Congratulations! The True Ending is yours!"
    }

    def __init__(self, screen: pygame.Surface, screen_size: tuple[int, int]) -> None:
        self._screen = screen
        self._screen_size = screen_size
        self._clock = pygame.time.Clock()

        # Adjusted font sizes for smaller screens
        self.title_font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 28)

        # Button setup (stacked vertically)
        self.button_width = 200
        self.button_height = 55
        center_x = screen_size[0] // 2

        self.restart_button_rect = pygame.Rect(
            center_x - self.button_width // 2,
            screen_size[1] // 2 + 40,
            self.button_width,
            self.button_height,
        )
        self.exit_button_rect = pygame.Rect(
            center_x - self.button_width // 2,
            self.restart_button_rect.bottom + 20,
            self.button_width,
            self.button_height,
        )

    def draw_button(self, rect: pygame.Rect, text: str, hover: bool = False):
        """Draws a button with hover effect and text."""
        color = self.LIGHT_GREY if hover else self.GREY
        pygame.draw.rect(self._screen, color, rect, border_radius=12)
        pygame.draw.rect(self._screen, self.WHITE, rect, width=2, border_radius=12)
        label = self.button_font.render(text, True, self.WHITE)
        label_rect = label.get_rect(center=rect.center)
        self._screen.blit(label, label_rect)

    def reset_game(self):
        """Completely clears game state before restarting."""
        from entities.entity_master import EntityMaster
        EntityMaster.clear_all()

        # Reset pygame display surface (optional but clean)
        self._screen.fill(self.BLACK)
        pygame.display.flip()

    def show(self, ending_type: str) -> None:
        """Display the appropriate ending and wait for user action."""
        text = self.ENDING_MESSAGES.get(ending_type, "Unknown Ending")
        running = True

        while running:
            self._screen.fill(self.BLACK)

            # Render main message (wrap long lines)
            wrapped_lines = self.wrap_text(text, self.title_font, self._screen_size[0] - 60)
            y_offset = self._screen_size[1] // 2 - 100

            for line in wrapped_lines:
                line_surface = self.title_font.render(line, True, self.WHITE)
                line_rect = line_surface.get_rect(center=(self._screen_size[0] // 2, y_offset))
                self._screen.blit(line_surface, line_rect)
                y_offset += 50

            # Handle hover
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
                        self.reset_game()
                        from main import main  # local import avoids circular import
                        main()
                    elif self.exit_button_rect.collidepoint(event.pos):
                        sys_exit()

            self._clock.tick(30)

    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        """Splits text into multiple lines if it's too wide."""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines