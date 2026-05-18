import json
import pygame

from cv2.typing import MatLike


class GameProperties:
    """game properties serializer"""
    # Base game properties
    _background_color: tuple[int, int, int]
    _difficulty: str

    # Screen
    _screen_size: tuple[int, int]
    _game_scale: float
    _width: int
    _height: int

    # Sprite
    _sprite_sheets: dict[str: MatLike] | None = None
    _char_sprite_sheets_path: dict[str: str] | None = None
    _sprite_properties: dict[str: int] | None = None
    _char_properties: dict[str: int] | None = None
    _sprite_scale: float | None = None

    # Controls
    _key_bindings: dict[str: str]

    _debug: bool

    # Entity props
    _entity_props: int

    # Dragon properties

    # Foes

    def __init__(self, char_sprite: str | None = None):
        with open("game_properties.json", "r") as jsonfile:
            self._settings = json.load(jsonfile)

            # Получаем разрешение экрана
            res: str = self._settings["GameProperties"]["ScreenSize"]
            self._game_scale = self._settings["GameProperties"]["Scale"]
            self._screen_size = tuple(map(int, res.split("*")))
            self._width, self._height = self._screen_size

            self._debug = self._settings["GameProperties"]["DEBUG"]

            # Получаем спрайт
            if char_sprite is not None:
                self._sprite_properties = self._settings["EntityProperties"][char_sprite]["Sprite_properties"]
                self._char_sprite_sheets_path = self._settings["EntityProperties"][char_sprite]["Sprite_properties"]["Frames_path"]
                self._sprite_scale = self._settings["EntityProperties"][char_sprite]["Sprite_properties"]["Scale"]

                # Получаем свойства игрока
                self._char_properties = self._settings["EntityProperties"][char_sprite]["Ingame_Properties"]

            # Получаем управление
            self._key_bindings = self._settings["GameProperties"]["Controls"]

    @property
    def debug(self) -> bool:
        return self._debug
    
    @property
    def sprite_scale(self) -> float:
        return self._sprite_scale

    @property
    def controls(self) -> dict[str, str]:
        controls = {action: getattr(pygame, key_name) for action, key_name in self._key_bindings.items()}
        return controls

    @property
    def game_scale(self) -> float:
        return self._game_scale
    
    @property
    def sprite_properties(self) -> dict[str, int]:
        return self._sprite_properties
    # @classmethod
    @property
    def char_properties(self) -> dict[str, int]:
        return self._char_properties
    
    @property
    def char_assets_pathes(self) -> dict[str, str]:
        return self._char_sprite_sheets_path

    @property
    def screen_size(self) -> tuple[int, int]:
        """Returns the scaled screen size as integers."""
        self._screen_size = int(self._width * self._game_scale), int(self._height * self._game_scale)
        return self._screen_size
    

if __name__ == "__main__":
    game_properties = GameProperties(char_sprite="Knight")
