import pygame
import math
from cv2.typing import MatLike

from utils import SpriteHandler, GameProperties
        

class BaseEntity(pygame.sprite.Sprite):
    """Base class for all entities in the game (player, enemies, etc.)"""
    _hp: int
    _attack: int
    _speed: int
    _hitbox: pygame.Rect
    _sprite: pygame.sprite.Sprite
    _animation: dict[str, MatLike]
    _controls: dict[str, int]
    _rect: pygame.Rect

    def __init__(self, hp: int, attack: int, speed: int, hitbox: pygame.Rect) -> None:
        super().__init__()
        self._hp = hp
        self._attack = attack
        self._speed = speed
        self._hitbox = hitbox

    # ----- HP -----
    @property
    def hp(self) -> int:
        return self._hp
    
    @hp.setter
    def hp(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("HP must be an integer!")
        self._hp = value

    # ----- Attack -----
    @property
    def attack(self) -> int:
        return self._attack
    
    @attack.setter
    def attack(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("Attack must be an integer!")
        self._attack = value

    # ----- Speed -----
    @property
    def speed(self) -> int:
        return self._speed
    
    @speed.setter
    def speed(self, value: int) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError("Speed must be numeric!")
        self._speed = value

    # ----- Hitbox -----
    @property
    def hitbox(self) -> pygame.Rect:
        return self._hitbox
    
    @hitbox.setter
    def hitbox(self, rect: pygame.Rect) -> None:
        if not isinstance(rect, pygame.Rect):
            raise ValueError("Hitbox must be a pygame.Rect!")
        self._hitbox = rect

    def draw_hitbox(self, surface: pygame.Surface) -> None:
        """Draw the hitbox for debugging."""
        pygame.draw.rect(surface, (255, 0, 0), self._hitbox, 2)

    def on_collision(self, other: "BaseEntity") -> None:
        """Called when this entity collides with another."""
        # Default behavior: just print (for debugging)
        print(f"{self.__class__.__name__} collided with {other.__class__.__name__}")


