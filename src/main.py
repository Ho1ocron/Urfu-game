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
        self._player = Knight(hp=10, attack=10, group=self.player_group, speed=10, init_pos=(50, 100))

        self._screen.fill((255, 255, 255))
        self.player_group.draw(self._screen)

        self._screen_rect = pygame.Rect((0,0), self.__screen_size)

        

    def run(self) -> None:
        
        keys = pygame.key.get_pressed()
        try: 
            self._player.handle_input(keys)
            self.player_group.update()
            # print(self._player.rect.x)
            self._screen.fill((255, 255, 255))  # clear previous frame
            self.player_group.draw(self._screen)
            self._player.rect.clamp_ip(self._screen_rect)
            
            if self._game_properties.debug == True:
                self._player.draw_hitbox(self._screen)
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