from sys import exit as sys_exit
import pygame

from utils import GameProperties
from entities import Knight


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
        self.__screen_size = self._game_properties.screen_size
        pygame.init()
        self._screen = pygame.display.set_mode(self.__screen_size)

        self.player_group = pygame.sprite.Group()
        # try:
        self._player = Knight(10, 10, [], group=self.player_group, speed=5)
        self._screen.fill((0, 0, 0))
        self.player_group.draw(self._screen)
        # except Exception as main_exception:
        #     print(f"{main_exception=}")
        

    def run(self) -> None:
        
        keys = pygame.key.get_pressed()
        try: 
            self._player.handle_input(keys)
            self.player_group.update()
            # print(self._player.rect.x)
            self._screen.fill(self.BLACK)  # clear previous frame
            self.player_group.draw(self._screen)
        except:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys_exit()
        
        
        pygame.display.flip()
        self.__clock.tick(25)        
    

def main() -> None:
    game = Game()

    while True:
        game.run()


if __name__ == "__main__":
    main()