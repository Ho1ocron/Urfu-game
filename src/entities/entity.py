import pygame
import numpy as np
from cv2.typing import MatLike

from utils import SpriteHandler, GameProperties


class BaseEntity:
    _hp: int
    _attack: int
    _hitbox: list
    _sprite: pygame.sprite.Sprite

    def __init__(self, hp: int, attack: int, hitbox: list) -> None:
        self._hp = hp
        self._attack = attack
        self._hitbox = hitbox
    
    @property
    def hp(self) -> int:
        return self._hp
    
    @hp.setter
    def hp(self, action: int) -> None:
        if not isinstance(action, int):
            raise ValueError("Action should be integer!")
            return
        
        self._hp = action


class Knight(pygame.sprite.Sprite):
    """Knight is a class for the player"""
    _hp: int
    _attack: int
    _sprite: pygame.sprite.Sprite
    _speed: int
    _init_pos: tuple[int]
    facing_right: bool = True
    _controls: dict[str: int]

    def __init__(self, hp: int, attack: int, group: pygame.sprite.Group, speed: int, init_pos: tuple[int]) -> None:
        super().__init__(group)
        self._hp = hp
        self._attack = attack
        self._speed = speed

        self.sprite_handler = SpriteHandler(char_sprite="Knight",)

        self.direction = "down"
        self.frame_index = 0
        self.animation_speed = 0.4

        self.game_props = GameProperties()
        self._controls = self.game_props.controls

        self.image = self._get_current_frame()
        self.rect = self.image.get_rect(center=init_pos)

        self.hitbox_margin = 0
        self.hitbox = pygame.Rect(
            self.rect.x + self.hitbox_margin,
            self.rect.y + self.hitbox_margin,
            self.rect.width - self.hitbox_margin,
            self.rect.height - self.hitbox_margin,
        )

    def _get_current_frame(self) -> pygame.Surface:
        """Return current pygame Surface for the knight’s facing direction."""
        frames = self.sprite_handler.animation["Walk"][self.direction]
        frame: MatLike = frames[int(self.frame_index)%len(frames)]
        if frame.shape[2] == 4:
            print("Transperant detected")
            alpha = frame[:, :, 3]
            y, x = np.where(alpha > 0)
            cropped = frame[np.min(y):np.max(y)+1, np.min(x):np.max(x)+1]
        else:
            print("Transperant not detected")
            print(frame.shape)
            cropped = frame  # fallback

        return pygame.image.frombuffer(cropped.tobytes(), frame.shape[1::-1], "RGB")
    
    def update_hitbox(self):
        """Recalculate hitbox position and size."""
        self.hitbox = pygame.Rect(
            self.rect.x + self.hitbox_margin,
            self.rect.y + self.hitbox_margin,
            self.rect.width - self.hitbox_margin * 2,
            self.rect.height - self.hitbox_margin * 2
        )
    
    def draw_hitbox(self, surface: pygame.Surface) -> None:
        """Draw the hitbox for debugging."""
        pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 2)
    
    def handle_input(self, keys) -> None:
        moving = False

        if keys[self._controls["Walk_left"]]:
            self.rect.x -= self._speed
            self.direction = "left"
            moving = True
        elif keys[self._controls["Walk_right"]]:
            self.rect.x += self._speed
            self.direction = "right"
            moving = True
        elif keys[self._controls["Walk_up"]]:
            self.rect.y -= self._speed
            self.direction = "up"
            moving = True
        elif keys[self._controls["Walk_down"]]:
            self.rect.y += self._speed
            self.direction = "down"
            moving = True
        if moving:
            self.frame_index += self.animation_speed
        else:
            self.frame_index = 0  # reset to idle

        # Cycle frames
        if self.frame_index >= len(self.sprite_handler.animation["Walk"][self.direction]):
            self.frame_index = 0

        # Update sprite image
        self.image = self._get_current_frame()

        # Update hitbox position
        # self.hitbox.topleft = (
        #     self.rect.x + self.hitbox_margin,
        #     self.rect.y + self.hitbox_margin
        # )
        self.update_hitbox()

