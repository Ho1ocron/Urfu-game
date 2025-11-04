import pygame
from sys import exit as sys_exit


class StartMenu:
    """Displays a start screen with controls, goal, and Proceed/Exit buttons."""

    def __init__(self, screen: pygame.Surface, screen_size: tuple[int, int]):
        self.screen = screen
        self.screen_size = screen_size
        self.clock = pygame.time.Clock()

        # Colors
        self.BACKGROUND = (10, 15, 30)  # dark blue-ish background
        self.TEXT_COLOR = (230, 230, 230)
        self.SUBTEXT_COLOR = (255, 100, 120)
        self.GOAL_COLOR = (120, 180, 255)
        self.BUTTON_COLOR = (50, 100, 180)
        self.BUTTON_HOVER = (80, 130, 210)
        self.EXIT_COLOR = (150, 50, 50)
        self.EXIT_HOVER = (200, 70, 70)

        # Define button rects
        self.proceed_rect = pygame.Rect(0, 0, 220, 60)
        self.exit_rect = pygame.Rect(0, 0, 220, 60)
        self.proceed_rect.center = (self.screen_size[0] // 2, self.screen_size[1] // 2 + 120)
        self.exit_rect.center = (self.screen_size[0] // 2, self.screen_size[1] // 2 + 200)

    def draw_text(self, text: str, size: int, color: tuple[int, int, int], center: tuple[int, int]):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center)
        self.screen.blit(text_surface, text_rect)

    def show(self) -> None:
        """Displays the start menu until the player presses Enter, clicks 'Proceed', or exits."""
        running = True
        while running:
            self.screen.fill(self.BACKGROUND)

            # Title
            self.draw_text("Knight vs Doppelgangers", 60, self.TEXT_COLOR,
                           (self.screen_size[0] // 2, 120))

            # Controls
            self.draw_text("Controls", 40, self.TEXT_COLOR,
                           (self.screen_size[0] // 2, 200))
            self.draw_text("Arrow Keys - Move", 28, self.SUBTEXT_COLOR,
                           (self.screen_size[0] // 2, 250))
            self.draw_text("Space - Shoot", 28, self.SUBTEXT_COLOR,
                           (self.screen_size[0] // 2, 280))
            self.draw_text("Shift - Dash", 28, self.SUBTEXT_COLOR,
                           (self.screen_size[0] // 2, 310))
            self.draw_text("Z - Heal", 28, self.SUBTEXT_COLOR,
                           (self.screen_size[0] // 2, 340))

            # Goal
            self.draw_text("Goal: Eliminate all your doppelgangers", 30, self.GOAL_COLOR,
                           (self.screen_size[0] // 2, 370))

            # Buttons
            mouse_pos = pygame.mouse.get_pos()

            # Proceed button
            if self.proceed_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, self.BUTTON_HOVER, self.proceed_rect, border_radius=15)
            else:
                pygame.draw.rect(self.screen, self.BUTTON_COLOR, self.proceed_rect, border_radius=15)
            self.draw_text("Proceed (Enter)", 36, (255, 255, 255), self.proceed_rect.center)

            # Exit button
            if self.exit_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, self.EXIT_HOVER, self.exit_rect, border_radius=15)
            else:
                pygame.draw.rect(self.screen, self.EXIT_COLOR, self.exit_rect, border_radius=15)
            self.draw_text("Exit (Esc)", 36, (255, 255, 255), self.exit_rect.center)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys_exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Enter starts the game
                        running = False
                    elif event.key == pygame.K_ESCAPE:  # Esc exits
                        sys_exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.proceed_rect.collidepoint(event.pos):
                        running = False  # Start game
                    elif self.exit_rect.collidepoint(event.pos):
                        sys_exit()  # Quit game

            pygame.display.flip()
            self.clock.tick(30)