import json


class GameProperties:
    """game properties serializer"""
    # Base game properties
    _background_color: tuple[int, int, int]
    _difficulty: str
    _screen_size: tuple[int, int]
    _scale: float
    _width: int
    _height: int

    _sprite_properties: dict[str: int]

    # Knight (player) properties

    # Dragon properties

    # Foes

    def __init__(self, char_sprite: str | None = None):
        with open("game_properties.json", "r") as jsonfile:
            self._settings = json.load(jsonfile)

            # Получаем разрешение экрана
            res: str = self._settings["GameProperties"]["ScreenSize"]
            self._scale = self._settings["GameProperties"]["Scale"]
            if char_sprite is not None:
                self._player_is_sprite_sheet: bool = self._settings["EntityProperties"]["Knight"]
                self._sprite_properties = self._settings["EntityProperties"][char_sprite]["Sprite_properties"]
            self._screen_size = tuple(map(int, res.split("*")))

            self._width, self._height = self._screen_size

    @property
    def scale(self):
        return self._scale
    
    @property
    def sprite_properties(self):
        return self._sprite_properties

    @property
    def screen_size(self):
        """Returns the scaled screen size as integers."""
        self._screen_size = int(self._width * self._scale), int(self._height * self._scale)
        print(f"Screen size computed: {self._screen_size}")
        return self._screen_size

    @property
    def player_is_sprite_sheet(self) -> bool:
        """Returns if player sprites are devided into each file or not"""
        return self._player_is_sprite_sheet
    

if __name__ == "__main__":
    game_properties = GameProperties(char_sprite="Knight")
