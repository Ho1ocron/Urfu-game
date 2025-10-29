from sys import exit as sys_exit
from datetime import datetime
import pygame


from utils import GameProperties
from entities import Knight, EnemyKnight, GroupManager, Bullet


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
        self._screen.fill((255, 255, 255))

        self._player = Knight(init_pos=(310-64//2, 375))
        self._enemy = EnemyKnight(init_pos=(100, 100))
        self._friend = Knight(init_pos=(300, 300))
        self._bullet = Bullet()

        self.group = GroupManager()
        GroupManager.all_sprites.draw(self._screen)

        self._screen_rect = pygame.Rect((0,0), self.__screen_size)

    def run(self) -> None:
        keys = pygame.key.get_pressed()
        self._player.handle_input(keys)
        self._screen.fill(self.BLACK)  # clear previous frame
        self._screen.blit(self._player.image, self._player.rect)
        self._screen.blit(self._enemy.image, self._enemy.rect)
        self._screen.blit(self._friend.image, self._friend.rect)
        self._screen.blit(self._bullet.image, self._friend.rect)

        self._player.rect.clamp_ip(self._screen_rect)
        GroupManager.check_collisions()

        if self._game_properties.debug:
            self._player.draw_hitbox(self._screen)
            self._enemy.draw_hitbox(self._screen)
            self._bullet.draw_hitbox(self._screen)

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