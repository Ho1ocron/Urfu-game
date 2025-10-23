from sys import exit as sys_exit
import pygame

from utils.settings import GameProperties


class Game:
    """Base class that controls the whole game."""
    _game_properties = GameProperties()
    _scale: float

    __screen_size: tuple[int, int]
    __screen: pygame.Surface
    __clock = pygame.time.Clock()

    BLACK = (0, 0, 0)

    def __init__(self) -> None:
        self.__screen_size = self._game_properties.screen_size

        pygame.init()
        try:
            self.__screen = pygame.display.set_mode(self.__screen_size)
        except:
            print(self.__screen_size)
            sys_exit()


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