import cv2
from cv2.typing import MatLike

from utils.settings import GameProperties

class SpriteHandler:
    _sprite_size: int = 192
    _total_sprites: int = 8
    _sprites_per_row: int = 3
    _sprites_bytes: list[bytes]
    _sprite_scale: float = 2

    _scale: float
    _sheet: MatLike
    _image: MatLike

    def __init__(self, sheet_path: str, scale: float = 1.0):
        game_properties = GameProperties()
        self._scale = game_properties.scale
        self._sprites_bytes = []

        self._sheet = cv2.imread(sheet_path, cv2.IMREAD_UNCHANGED)
        
        if self._sheet is None:
            raise ValueError(f"Failed to load sprite sheet: {sheet_path}")

        # Crop the sprite
        x = 0
        y = 0
        self._image = self._sheet[y:y+64, x:x+64]
        self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2RGB)
        self._image = cv2.resize(self._image, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
        self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2RGB)
        

    @property
    def sprite(self):
        return self._image
        # sprite = pygame.image.frombuffer(resized.tobytes(), resized.shape[1::-1], 'RGB')

