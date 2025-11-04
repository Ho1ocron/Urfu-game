from sys import exit as sys_exit
import pygame

from utils import GameProperties
from entities import Knight, Doppelganger, EntityMaster, Dragon
from gui import HPBar
from gui import StartMenu


class Game(pygame.sprite.Group):
    """Base class that controls the whole game."""
    _game_properties = GameProperties()
    _scale: float

    __screen_size: tuple[int, int]
    _screen: pygame.Surface
    __clock = pygame.time.Clock()

    BLACK = (0, 0, 0)

    def __init__(self) -> None:
        super().__init__()
        pygame.init()

        self.__screen_size = self._game_properties.screen_size
        self._screen = pygame.display.set_mode(self.__screen_size)
        pygame.display.set_caption("Knight vs Doppelgangers")

        # Show start UI
        start_menu = StartMenu(self._screen, self.__screen_size)
        start_menu.show()

        # Initialize game
        self._player = Knight(init_pos=(310 - 64 // 2, 375))
        for i in range(5):
            self._enemy = Doppelganger(_id=f"Enemy{i}")

        self._dragon = Dragon()

        EntityMaster.all_sprites.draw(self._screen)
        self._screen_rect = pygame.Rect((0, 0), self.__screen_size)
        self.hp_bar = HPBar(self._player, self._screen, pos=(self.__screen_size[0] - 220, 20))

    def run(self) -> None:
        keys = pygame.key.get_pressed()
        self._player.handle_input(keys)
        EntityMaster.all_sprites.update()

        self._player.rect.clamp_ip(self._screen_rect)
        EntityMaster.check_collisions()

        self._screen.fill(self.BLACK)
        EntityMaster.all_sprites.draw(self._screen)

        if self._game_properties.debug:
            self._player.draw_hitbox(self._screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys_exit()

        self.hp_bar.draw()
        pygame.display.flip()
        self.__clock.tick(25)


def main() -> None:
    game = Game()
    while True:
        game.run()


if __name__ == "__main__":
    main()