import pygame
import math
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
    _hp: int = 1
    _attack: int = 1
    _sprite: pygame.sprite.Sprite
    _speed: int = 1
    _init_pos: tuple[int]
    facing_right: bool = True
    _controls: dict[str: int]
    _animation: dict[str: MatLike]

    def __init__(self, group: pygame.sprite.Group, init_pos: tuple[int], x: bool = False) -> None:
        super().__init__(group)
        self.x = x

        self.sprite_handler = SpriteHandler(char_sprite="Knight",)

        self.direction = "down"
        self.frame_index = 0
        self.animation_speed = 0.4
        self._animation = self.sprite_handler.animation

        self.game_props = GameProperties("Knight")
        self._controls = self.game_props.controls
    # try: 
        self._hp = self.game_props.char_properties["HP"]
        self._attack = self.game_props.char_properties["Attack"]
        self._speed = self.game_props.char_properties["Speed"]
        # except Exception as e:
        #     print(e)

        self.image = self._get_current_frame()
        self.rect = self.image.get_rect(center=init_pos)

        self.hitbox_margin = 42
        self.hitbox = pygame.Rect(
            self.rect.x + self.hitbox_margin,
            self.rect.y + self.hitbox_margin,
            self.rect.width - self.hitbox_margin,
            self.rect.height - self.hitbox_margin,
        )

    def _get_current_frame(self, action: str = "Walk") -> pygame.Surface:
        """Return current pygame Surface for the knight’s facing direction."""
        frames = self._animation[action][self.direction]
        # self.sprite_handler.animation Вызывается постоянно. Переделать
        frame: MatLike = frames[int(self.frame_index)%len(frames)] 
        return pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGBA")
    
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

        dx, dy = 0, 0 # Are needed to impalement normalized diagonal speed
        if keys[self._controls["Walk_left"]]:
            dx -= 1
            self.direction = "left"
            moving = True
        if keys[self._controls["Walk_right"]]:
            dx += 1
            self.direction = "right"
            moving = True
        if keys[self._controls["Walk_up"]]:
            dy -= 1
            self.direction = "up"
            moving = True
        if keys[self._controls["Walk_down"]]:
            dy += 1
            self.direction = "down"
            moving = True
        if moving:
            self.frame_index += self.animation_speed
        
        # This is needed for normalizing the diagonal movement speed, since diagonal speed is faster due to sqrt(x^2+ y^2)
        if dx != 0 or dy != 0:
            magnitude = math.sqrt(dx**2 + dy**2)
            dx /= magnitude
            dy /= magnitude

            self.rect.x += dx * self._speed
            self.rect.y += dy * self._speed

            self.frame_index += self.animation_speed

        current_action = "Walk" if moving else "Idle"

        # Cycle frames
        self.frame_index += self.animation_speed if moving else 0.2  # idle can animate slower
        if self.frame_index >= len(self._animation[current_action][self.direction]):
            self.frame_index = 0
        # Update sprite image
        self.image = self._get_current_frame(action=current_action)

        # Update hitbox position
        self.hitbox.topleft = (
            self.rect.x + self.hitbox_margin,
            self.rect.y + self.hitbox_margin
        )
        self.update_hitbox()

