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
    _sprite: pygame.Surface
    _animation: dict[str, MatLike]
    _controls: dict[str, int]

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


class Knight(BaseEntity):
    """Knight is a controllable player character."""

    facing_right: bool = True

    def __init__(self, group: pygame.sprite.Group, init_pos: tuple[int], x: bool = False) -> None:
        # Initialize sprite
        pygame.sprite.Sprite.__init__(self, group)


        # Initialize handler and properties
        self.sprite_handler = SpriteHandler(char_sprite="Knight")
        self.game_props = GameProperties("Knight")

        # Load game properties
        hp = self.game_props.char_properties["HP"]
        attack = self.game_props.char_properties["Attack"]
        speed = self.game_props.char_properties["Speed"]
        self._controls = self.game_props.controls
        self._animation = self.sprite_handler.animation

        # Temporary dummy hitbox for parent init
        dummy_hitbox = pygame.Rect(0, 0, 64, 64)

        # Initialize BaseEntity
        BaseEntity.__init__(self, hp=hp, attack=attack, speed=speed, hitbox=dummy_hitbox)

        # Animation setup
        self.direction = "down"
        self.frame_index = 0
        self.animation_speed = 0.4

        self.image = self._get_current_frame()
        self.rect = self.image.get_rect(center=init_pos)

        # Hitbox setup
        self.hitbox_margin = 42
        self.update_hitbox()

        self.x = x

    def _get_current_frame(self, action: str = "Walk") -> pygame.Surface:
        """Return current pygame Surface for the knight’s facing direction."""
        frames = self._animation[action][self.direction]
        frame: MatLike = frames[int(self.frame_index) % len(frames)]
        return pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGBA")

    def update_hitbox(self) -> None:
        """Recalculate hitbox position and size."""
        self._hitbox = pygame.Rect(
            self.rect.x + self.hitbox_margin,
            self.rect.y + self.hitbox_margin,
            self.rect.width - self.hitbox_margin * 2,
            self.rect.height - self.hitbox_margin * 2
        )

    def handle_input(self, keys) -> None:
        """Handle keyboard input for movement and animation."""
        moving = False
        dx, dy = 0, 0

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

        # Normalize diagonal movement
        if dx != 0 or dy != 0:
            magnitude = math.sqrt(dx ** 2 + dy ** 2)
            dx /= magnitude
            dy /= magnitude

            self.rect.x += dx * self._speed
            self.rect.y += dy * self._speed

            self.frame_index += self.animation_speed

        current_action = "Walk" if moving else "Idle"
        self.frame_index += self.animation_speed if moving else 0.2

        # Reset frame index when looping animation
        if self.frame_index >= len(self._animation[current_action][self.direction]):
            self.frame_index = 0

        # Update image and hitbox
        self.image = self._get_current_frame(action=current_action)
        self.update_hitbox()


class EnemyKnight(BaseEntity):
    """Generic enemy class."""

    def __init__(self, group: pygame.sprite.Group, init_pos: tuple[int], sprite_name: str = "Knight"):
        pygame.sprite.Sprite.__init__(self, group)
        self.sprite_handler = SpriteHandler(char_sprite=sprite_name)
        self.game_props = GameProperties(sprite_name)

        hp = self.game_props.char_properties["HP"]
        attack = self.game_props.char_properties["Attack"]
        speed = self.game_props.char_properties["Speed"]

        dummy_hitbox = pygame.Rect(0, 0, 64, 64)
        BaseEntity.__init__(self, hp=hp, attack=attack, speed=speed, hitbox=dummy_hitbox)

        self._animation = self.sprite_handler.animation
        self.direction = "down"
        self.frame_index = 0
        self.image = self._get_current_frame("Idle")
        self.rect = self.image.get_rect(center=init_pos)
        self.update_hitbox()

    def _get_current_frame(self, action: str = "Idle") -> pygame.Surface:
        frames = self._animation[action][self.direction]
        frame = frames[int(self.frame_index) % len(frames)]
        return pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGBA")

    def update_hitbox(self):
        self.hitbox = pygame.Rect(
            self.rect.x + 42, self.rect.y + 42,
            self.rect.width - 84, self.rect.height - 84
        )