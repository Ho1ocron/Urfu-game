import cv2
from cv2.typing import MatLike
import numpy as np


class SpriteHandler:
    _sprite_size: int = 192
    _total_sprites: int = 8
    _sprites_per_row: int = 3
    _sprites_bytes: list[bytes]

    _scale: float
    _sheet: MatLike
    _image: MatLike

    def __init__(self, sheet_path: str, scale: float = 1.0):
        self._scale = scale
        self._sprites_bytes = []

        # Load sprite sheet (with alpha channel if present)
        self._sheet = cv2.imread(sheet_path, cv2.IMREAD_UNCHANGED)
        if self._sheet is None:
            raise ValueError(f"Failed to load sprite sheet: {sheet_path}")

        # Extract each sprite and store as bytes
        for i in range(self._total_sprites):
            row = i // self._sprites_per_row
            col = i % self._sprites_per_row

            x = col * self._sprite_size
            y = row * self._sprite_size

            sprite = self._sheet[y:y+self._sprite_size, x:x+self._sprite_size]

            # Scale sprite if needed
            if self._scale != 1.0:
                width = int(self._sprite_size * self._scale)
                height = int(self._sprite_size * self._scale)
                sprite = cv2.resize(sprite, (width, height), interpolation=cv2.INTER_AREA)
            
            sprite = sprite.tobytes()
            self._sprites_bytes.append(sprite)

        print(f"Loaded {len(self._sprites_bytes)} sprites into memory as bytes.")

    @property
    def sprite(self):
        return self._sprites_bytes[0]
        # sprite = pygame.image.frombuffer(resized.tobytes(), resized.shape[1::-1], 'RGB')