import json
from cv2.typing import MatLike


class GameProperties:
    """game properties serializer"""
    # Base game properties
    _background_color: tuple[int, int, int]
    _difficulty: str
    _screen_size: tuple[int, int]
    _game_scale: float
    _width: int
    _height: int
    _sprite_sheets: dict[str: MatLike] 
    _sprite_properties: dict[str: int]
    _char_properties: dict[str: int]

    # Knight (player) properties

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

            # Получаем спрайт
            if char_sprite is not None:
                self._sprite_properties = self._settings["EntityProperties"][char_sprite]["Sprite_properties"]
                self._char_properties = self._settings["EntityProperties"][char_sprite]["Ingame_Properties"]
            

    @property
    def game_scale(self) -> float:
        return self._game_scale
    
    @property
    def sprite_properties(self) -> dict[str: int]:
        return self._sprite_properties
    
    @property
    def char_properties(self) -> dict[str: int]:
        return self._char_properties

    @property
    def screen_size(self) -> tuple[int, int]:
        """Returns the scaled screen size as integers."""
        self._screen_size = int(self._width * self._game_scale), int(self._height * self._game_scale)
        return self._screen_size
    

if __name__ == "__main__":
    game_properties = GameProperties(char_sprite="Knight")
