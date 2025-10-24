from sys import exit as sys_exit
import pygame

from utils.settings import GameProperties
from utils.sprite_handler import SpriteHandler
from entities.entity import Knight


class Game(pygame.sprite.Group):
    """Base class that controls the whole game."""
    _game_properties = GameProperties()
    _scale: float

    __screen_size: tuple[int, int]
    __screen: pygame.Surface
    __clock = pygame.time.Clock()

    BLACK = (0, 0, 0)

    def __init__(self) -> None:
        super().__init__()
        self.__screen_size = self._game_properties.screen_size
        pygame.init()
        self.__screen = pygame.display.set_mode(self.__screen_size)

        self.player_group = pygame.sprite.Group()
        self._player = Knight(10, 10, [], group=self.player_group)


    def run(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys_exit()
        
        self.__screen.fill((0, 0, 0))
        pygame.display.flip()
        self.__clock.tick(25)        
    

def main() -> None:
    game = Game()

    while True:
        game.run()


if __name__ == "__main__":
    main()