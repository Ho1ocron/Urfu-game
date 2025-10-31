import pygame

class HPBar:
    """Displays a health bar for the player."""
    def __init__(self, player, screen, pos=(0, 0), size=(150, 20), color=(255, 0, 102), bg_color=(102, 0, 51)) -> None:
        self.player = player
        self.screen = screen
        self.pos = pos
        self.size = size
        self.color = color
        self.bg_color = bg_color
        self.border_color = (50, 50, 50)

    def draw(self) -> None:
        """Draw the HP bar based on player's current health."""
        current_hp = self.player.hp
        max_hp = self.player.max_hp
        x, y = self.pos
        x += 30
        w, h = self.size

        # Draw background
        pygame.draw.rect(self.screen, self.bg_color, (x, y, w, h))
        pygame.draw.rect(self.screen, self.border_color, (x, y, w, h), 3)

        # Calculate width of current HP
        hp_width = int((current_hp / max_hp) * (w - 4))
        pygame.draw.rect(self.screen, self.color, (x + 2, y + 2, hp_width, h - 4))