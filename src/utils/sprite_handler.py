from datetime import datetime
import numpy as np
from cv2.typing import MatLike
from cv2 import (
    imread,
    resize,
    cvtColor,
    IMREAD_UNCHANGED,
    INTER_NEAREST,
    COLOR_BGRA2RGBA,
)

from utils.settings import GameProperties


class SpriteHandler:
    _sprite_size: int = 192
    _total_sprites: int = 8
    _sprites_per_row: int = 3
    _sprite_scale: float = 2
    _sprites_bytes: list[bytes]

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

    def __init__(self, char_sprite: str, scale: float = 1.0) -> None:
        game_properties = GameProperties(char_sprite=char_sprite)

        sprite_properties = game_properties.sprite_properties
        sprite_sheets_pathes: dict[str: str] = game_properties.char_assets_pathes

        self.SPRITE_WIDTH: int = sprite_properties["Sprite_width"]
        self.SPRITE_HEIGHT: int = sprite_properties["Sprite_height"]
        self.NUM_SPRITES: int = sprite_properties["Num_sprites"]

        self._sprites_per_row: int = sprite_properties["Sprites_per_row"]
        self._sprite_scale: float = sprite_properties["Scale"]

        self._scale = game_properties.game_scale
        # self._sprite_properties
        self._sprites_bytes = []
        self._sprite_sheets = {
            "Walk": {
                "up": imread(sprite_sheets_pathes["Walk"]["up"], IMREAD_UNCHANGED),
                "down": imread(sprite_sheets_pathes["Walk"]["down"], IMREAD_UNCHANGED),
                "left": imread(sprite_sheets_pathes["Walk"]["left"], IMREAD_UNCHANGED),
                "right": imread(sprite_sheets_pathes["Walk"]["right"], IMREAD_UNCHANGED),
            },
            "Idle": {
                "up": imread(sprite_sheets_pathes["Idle"]["up"], IMREAD_UNCHANGED),
                "down": imread(sprite_sheets_pathes["Idle"]["down"], IMREAD_UNCHANGED),
                "left": imread(sprite_sheets_pathes["Idle"]["left"], IMREAD_UNCHANGED),
                "right": imread(sprite_sheets_pathes["Idle"]["right"], IMREAD_UNCHANGED),
            }
        }

    def _extract_sprites(self, sheet, sprite_width, sprite_height, count) -> list[MatLike]:
        sprites: list[MatLike] = []
        for i in range(count):
            x = i * sprite_width
            y = 0  # since we have only one row
            try:
                sprite = sheet[y:y + sprite_height, x:x + sprite_width]
                sprite = resize(sprite, None, fx=self._sprite_scale, fy=self._sprite_scale, interpolation=INTER_NEAREST)
                sprite = cvtColor(sprite, COLOR_BGRA2RGBA)
                sprites.append(sprite)
            except Exception as sprite_handler:
                time = datetime.now()
                print(f"{sprite_handler=}, time: {time.strftime("%M:%S")}")
    
        return sprites
    
    @property
    def animation(self) -> dict[str: list[MatLike]]:
        animation_walk_up = self._extract_sprites(self._sprite_sheets["Walk"]["up"], self.SPRITE_WIDTH, self.SPRITE_HEIGHT, self.NUM_SPRITES)
        animation_walk_down = self._extract_sprites(self._sprite_sheets["Walk"]["down"], self.SPRITE_WIDTH, self.SPRITE_HEIGHT, self.NUM_SPRITES)
        animation_walk_left = self._extract_sprites(self._sprite_sheets["Walk"]["left"], self.SPRITE_WIDTH, self.SPRITE_HEIGHT, self.NUM_SPRITES)
        animation_walk_right = self._extract_sprites(self._sprite_sheets["Walk"]["right"], self.SPRITE_WIDTH, self.SPRITE_HEIGHT, self.NUM_SPRITES)
        #----------Idle----------#
        animation_idle_up = self._extract_sprites(self._sprite_sheets["Idle"]["up"], self.SPRITE_WIDTH, self.SPRITE_HEIGHT, self.NUM_SPRITES)
        animation_idle_down = self._extract_sprites(self._sprite_sheets["Idle"]["down"], self.SPRITE_WIDTH, self.SPRITE_HEIGHT, self.NUM_SPRITES)
        animation_idle_left = self._extract_sprites(self._sprite_sheets["Idle"]["left"], self.SPRITE_WIDTH, self.SPRITE_HEIGHT, self.NUM_SPRITES)
        animation_idle_right = self._extract_sprites(self._sprite_sheets["Idle"]["right"], self.SPRITE_WIDTH, self.SPRITE_HEIGHT, self.NUM_SPRITES)
        
        return {
            "Walk": {
                "up": animation_walk_up,
                "down": animation_walk_down,
                "left": animation_walk_left,
                "right": animation_walk_right
            },
            "Idle": {
                "up": animation_idle_up,
                "down": animation_idle_down,
                "left": animation_idle_left,
                "right": animation_idle_right
            }
        }

    @property
    def sprite(self):
        return self._image