from sys import exit as sys_exit
import pygame
import pygame._freetype as _freetype
from cv2 import imread, resize, cvtColor, IMREAD_UNCHANGED, INTER_NEAREST, COLOR_BGRA2RGBA

from utils import GameProperties
from entities import Knight, Doppelganger, EntityMaster, Dragon
from gui import HPBar, StartMenu
from gui import EndingScreen 


class Game(pygame.sprite.Group):
    """Base class that controls the whole game."""
    _game_properties = GameProperties()
    _scale: float

    __screen_size: tuple[int, int]
    _screen: pygame.Surface
    __clock = pygame.time.Clock()

    BLACK = (10, 15, 30)

    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        _freetype.init()

        self.__screen_size = self._game_properties.screen_size
        self._screen = pygame.display.set_mode(self.__screen_size)
        pygame.display.set_caption("Knight vs Doppelgangers")

        # Show start UI
        start_menu = StartMenu(self._screen, self.__screen_size)
        start_menu.show()

        # Initialize game
        self._player = Knight(init_pos=(310 - 64 // 2, 375))
        for i in range(7):
            self._enemy = Doppelganger(_id=f"Enemy{i}")

        self._dragon = Dragon()

        EntityMaster.all_sprites.draw(self._screen)
        self._screen_rect = pygame.Rect((0, 0), self.__screen_size)
        self.hp_bar = HPBar(self._player, self._screen, pos=(self.__screen_size[0] - 220, 20))

        # add background surface
        sheet = imread("assets/Sprites/GRASS+.png", IMREAD_UNCHANGED)
        raw_tile = sheet[8 * 16:(8 + 1) * 16, 17 * 16:(17 + 1) * 16]
        scale = self._game_properties.game_scale
        tile_size = int(16 * scale)
        raw_tile = resize(raw_tile, (tile_size, tile_size), interpolation=INTER_NEAREST)
        raw_tile = cvtColor(raw_tile, COLOR_BGRA2RGBA)
        scaled_tile = pygame.image.frombuffer(raw_tile.tobytes(), (tile_size, tile_size), "RGBA")
        sw, sh = self.__screen_size
        self._bg = pygame.Surface((sw, sh))
        for ty in range(0, sh, tile_size):
            for tx in range(0, sw, tile_size):
                self._bg.blit(scaled_tile, (tx, ty))

        # Game state
        self.running = True
        self.ending_type = None
        self.ending_screen = EndingScreen(self._screen, self.__screen_size)

    def check_end_conditions(self):
        """Determine if the game should end."""
        player_alive = self._player.alive()
        dragon_alive = self._dragon.alive()
        enemies_alive = any(enemy.alive() for enemy in EntityMaster.enemy_group)

        if not player_alive:
            self.ending_type = "bad"
            self.running = False
        elif not dragon_alive and enemies_alive:
            self.ending_type = "good"
            self.running = False
        elif not dragon_alive and not enemies_alive:
            self.ending_type = "true"
            self.running = False

    def run(self) -> None:
        if not self.running:
            self.ending_screen.show(self.ending_type)
            return

        keys = pygame.key.get_pressed()
        self._player.handle_input(keys)
        EntityMaster.all_sprites.update()

        self._player.rect.clamp_ip(self._screen_rect)
        EntityMaster.check_collisions()
        self.check_end_conditions()

        self._screen.blit(self._bg, (0, 0))
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