from sys import exit as sys_exit
from datetime import datetime
import pygame


from utils import GameProperties
from entities import Knight, EnemyKnight, GroupManager


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

        # self.player_group = pygame.sprite.Group()
        # self.enemy_group = pygame.sprite.Group()

        self._player = Knight(init_pos=(310-64//2, 375))
        self._enemy = EnemyKnight(init_pos=(100, 100))

        self._screen.fill((255, 255, 255))
        self.group = GroupManager()
        GroupManager.all_sprites.draw(self._screen)
        # self.group.player_group.draw(self._screen)
        # self.group.enemy_group.draw(self._screen)

        self._screen_rect = pygame.Rect((0,0), self.__screen_size)

        self.draw_hitbox = False
        self.key_pressed = False

    def hitbox_collision(self, sprite1, sprite2):
        return sprite1.hitbox.colliderect(sprite2.hitbox) 

    def run(self) -> None:
        keys = pygame.key.get_pressed()
        self._player.handle_input(keys)
        self._screen.fill(self.BLACK)  # clear previous frame
        self._screen.blit(self._player.image, self._player.rect)
        self._screen.blit(self._enemy.image, self._enemy.rect)
        self._player.rect.clamp_ip(self._screen_rect)
        GroupManager.check_collisions()

        if keys[pygame.K_0]:
            if self.key_pressed == False:
                self.draw_hitbox = True
                self.key_pressed = True
            else:
                self.draw_hitbox = False
                self.key_pressed = False

        if True:
            self._player.draw_hitbox(self._screen)
            self._enemy.draw_hitbox(self._screen)

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