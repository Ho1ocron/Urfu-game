from sys import exit as sys_exit
import pygame


class Game:
    """Base class that controls the whole game."""
    _scale: float
    _width: int
    _height: int

    __screen_size: tuple[int, int]
    __screen: pygame.Surface
    __clock = pygame.time.Clock()

    BLACK = "#301934"

    def __init__(self, scale: float, width: int, height: int) -> None:
        self._scale = scale
        self._width = width
        self._height = height
        self.__screen_size = int(self._width * self._scale), int(self._height * self._scale)

        pygame.init()
        self.__screen = pygame.display.set_mode(self.__screen_size)


    def run(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys_exit()
        
        self.__screen.fill(self.BLACK)
        pygame.display.flip()
        self.__clock.tick(25)        
    

def main() -> None:
    game = Game(2.5, 310, 246)

    while True:
        game.run()


if __name__ == "__main__":
    main()