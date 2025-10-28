from cv2.typing import MatLike
from cv2 import (
    imread,
    resize,
    cvtColor,
    IMREAD_UNCHANGED,
    INTER_NEAREST,
    COLOR_BGRA2RGB,
)

from utils.settings import GameProperties

class SpriteHandler:
    _sprite_size: int = 192
    _total_sprites: int = 8
    _sprites_per_row: int = 3
    _sprites_bytes: list[bytes]
    _sprite_scale: float = 2

    _scale: float
    
    SPRITE_WIDTH: int
    SPRITE_HEIGHT: int
    NUM_SPRITES: int

    _sprite_properties: dict[str: int]
    #--------Sprites--------#
    _sprite_sheets: dict[str: MatLike]
    _image: MatLike
    #-----------animation frame lists------------#
    _animation_up = list[MatLike]
    _animation_down = list[MatLike]
    _animation_left = list[MatLike]
    _animation_right = list[MatLike]


    def __init__(
        self, 
        char_sprite: str, 
        walk_sheet_path_up: str, 
        walk_sheet_path_down: str, 
        walk_sheet_path_left: str, 
        walk_sheet_path_right: str, 
        scale: float = 1.0
    ) -> None:
        game_properties = GameProperties(char_sprite=char_sprite)

        sprite_properties = game_properties.sprite_properties

        self.SPRITE_WIDTH: int = sprite_properties["SPRITE_WIDTH"]
        self.SPRITE_HEIGHT: int = sprite_properties["SPRITE_HEIGHT"]
        self.NUM_SPRITES: int = sprite_properties["NUM_SPRITES"]

        self._scale = game_properties.game_scale
        # self._sprite_properties
        self._sprites_bytes = []
        self._sprite_sheets = {
            "up": imread(walk_sheet_path_up, IMREAD_UNCHANGED),
            "down": imread(walk_sheet_path_down, IMREAD_UNCHANGED),
            "left": imread(walk_sheet_path_left, IMREAD_UNCHANGED),
            "right": imread(walk_sheet_path_right, IMREAD_UNCHANGED),
        }


        # # Crop the sprite
        # x = 0
        # y = 0
        # self._image = self._sheet_up[y:y+48, x:x+64]
        # self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2RGB)
        # self._image = cv2.resize(self._image, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
        # self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2RGB)

    def _extract_sprites(self, sheet, sprite_width, sprite_height, count) -> list[MatLike]:
        sprites: list[MatLike] = []
        for i in range(count):
            x = i * sprite_width
            y = 0  # assuming one row
            try:
                sprite = sheet[y:y + sprite_height, x:x + sprite_width]
                sprite = resize(sprite, None, fx=2.5, fy=2.5, interpolation=INTER_NEAREST)
                sprite = cvtColor(sprite, COLOR_BGRA2RGB)
            except Exception as sprite_handler:
                print(f"{sprite_handler=}")
            sprites.append(sprite)
        return sprites
    
    @property
    def animation(self) -> dict[str: MatLike]:
        animation_up = self._extract_sprites(self._sprite_sheets["up"], self.SPRITE_WIDTH, self.SPRITE_HEIGHT, self.NUM_SPRITES)
        animation_down = self._extract_sprites(self._sprite_sheets["down"], self.SPRITE_WIDTH, self.SPRITE_HEIGHT, self.NUM_SPRITES)
        animation_left = self._extract_sprites(self._sprite_sheets["left"], self.SPRITE_WIDTH, self.SPRITE_HEIGHT, self.NUM_SPRITES)
        animation_right = self._extract_sprites(self._sprite_sheets["right"], self.SPRITE_WIDTH, self.SPRITE_HEIGHT, self.NUM_SPRITES)
        return {
            "up": animation_up,
            "down": animation_down,
            "left": animation_left,
            "right": animation_right
        }

        

    @property
    def sprite(self):
        return self._image
        # sprite = pygame.image.frombuffer(resized.tobytes(), resized.shape[1::-1], 'RGB')

